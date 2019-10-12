#!/usr/bin/python3

import cgi,cgitb
import psycopg2
import re
import datetime
from passlib.hash import pbkdf2_sha256
import requests
import json
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def reCAPTCHA(g_response):
	url = 'https://www.google.com/recaptcha/api/siteverify'
	payload = {'secret' :'6LclYLoUAAAAAH9eix2giVphRCUAj0I9me0azjkz','response':g_response}

	try:
		r = requests.get(url,params=payload)
		r_dict = r.json()
		status = r_dict['success']
		
		if status == False:
			return False
		else:
			return True
	except:
		return False

def newCustomer(email,user,psw,name,lname,bday,gender,phone,address,key):
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
		
		cursor = connection.cursor()
		hash = pbkdf2_sha256.hash(psw)
		psw = hash
		cursor.execute("insert into customers\
		 (email,username,password,name,lname,bday,gender,phone,address,conf_token,last_pass_change)\
		values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		,(email,user,psw,name,lname,bday,gender,phone,address,key,"now()"))
		connection.commit()
		return True

	except(Exception,psycopg2.IntegrityError) as err:
		return False
		
	except(Exception,psycopg2.Error) as error:
		print("Error while connecting to PostgreSQL:",error)

	finally:
		if connection:
			cursor.close()
			connection.close()

def lengthCheck(attr,max):
	if len(attr) <= max:
		return True
	else:
		return False

def validateDate(date):
	index = date.find('-')
	year = date[:index]
	year = int(year)
	currentyear = str(datetime.date.today())
	index = currentyear.find('-')
	currentyear = currentyear[:index]
	currentyear = int(currentyear)
	if year >= currentyear - 100 and year <= currentyear:
		return True
	else:
		return False 

def validatePhone(tel1,tel2,tel3):
	if len(str(tel1)) == 2 and len(str(tel2)) == 3 and len(str(tel3)) == 4:
		return True
	else:
		return False	

def generateKey():
	hexals = ['0','1','2','3','4','5','6','7','8','9'\
	,'A','B','C','D','E','F','a','b','c','d','e','f']
	
	length = 32
	key = ""
	for i in range(length):
		key += random.choice(hexals)
	return key
	

def sendMail(email,key): 
	link = 'http://127.0.0.1:8000/cgi-bin/activation.py?email=%s&token=%s'%(email,key)


	sender_email = "boyan.milanov@yandex.com"
	receiver_email = "boyan.milanov@yandex.com" #emal
	password = "Parola42"
	
	message = MIMEMultipart("alternative")
	message["Subject"] = "Activate your account"
	message["From"] = "boyan.milanov@yandex.com"
	message["To"] = "boyan.milanov@yandex.com"
	
	text = """\
	Hi,
	Click the link below to activate your account.
	---
	Note:
	If you have not registered on this site do nothing!"""
	html = """\
	<html>
	  <body>
	    <p>Hello,<br>
	      Click the link below to activate your account.<br>
	       <a href="%s">Click here</a> <br>
	       Note:<br>
	If you have not registered on this site do nothing!
	    </p>
	   <img src="Hello-Transparent.png" alt="hi"> 
	  </body>
	</html>
	"""%(link)
	
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	
	message.attach(part1)
	message.attach(part2)
	
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )



form = cgi.FieldStorage()

email = form.getvalue('email')
match = re.match('^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$',email)


user = form.getvalue('user')

name = form.getvalue('name')

lname = form.getvalue('lname')

gender = form.getvalue('gender')

bday = form.getvalue('bday')

code = form.getvalue('countryCode')
tel1 = form.getvalue('tel1')
tel2 = form.getvalue('tel2')
tel3 = form.getvalue('tel3')
phone = str(code) + str(tel1)+ str(tel2)+str(tel3)


address = form.getvalue('address')

psw = form.getvalue('psw')

conf_psw = form.getvalue('psw-repeat')

g_response = form.getvalue('g-recaptcha-response')

check = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
checkIndexMeanings=["Invalid e-mail","E-mail or username already in use"
,"The username already exists. Please use a different username",
"Password and Repeat Password don't match", "Username cannot be longer than 30 characters",
"First name cannot be longer than 30 characters","Invalid date",
"Invalid phone number","Address cannot be longer than 30 characters",
"Last name cannot be longer than 30 characters","Password must be at least 8 characters long",
"Password must contain at least 1 Capital Letter",
"Password must contain at least 1 Small-Case Letter","Password must contain letters",
"Please check out the reCAPTCHA","Password cannot contain the username"]

if match == None: 
	check[0] = False
	

if not lengthCheck(user,30):
	check[4] = False

if not lengthCheck(name,30):
	check[5] = False

if not validateDate(bday):
	check[6] = False


if not lengthCheck(address,30):
	check[8] = False

if not lengthCheck(lname,30):
	check[9] = False	

if not validatePhone(tel1,tel2,tel3):
	check[7] = False


if len(psw) < 8:
	check[10] = False

else:
	if psw != conf_psw:
		check[3] = False

	else:
		if psw.find(user) != -1:
			check[15] = False
		else:	
			if not psw.upper().isupper():
				check[13] = False
			else:
				if psw.islower():
					check[11] = False

				if psw.isupper():
					check[12] = False	

			 

if g_response == None:
	check[14] = False

else:	
	if reCAPTCHA(g_response) is False:
		check[14] = False



if gender == 'male':
	gender = 'm'
else:
	gender = 'f'	


validation = True
for i in check:
	if i is False:
		validation = False

if(validation):

	key = generateKey()
	unique = newCustomer(email,user,psw,name,lname,bday,gender,phone,address,key)

	if unique is True:
		plusSign = email.find('+')
		if plusSign != -1:
			newMail = email[:plusSign] + '%2B' + email[plusSign+1:]
			sendMail(newMail,key)
		else:
			sendMail(email,key)

		print("""Content-type:text/html\r\n\r\n
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="../reg_form.css">
	</head>
	<body>
		<div id="wrapper">
			<div class="container">
				<h1>Successful Registration</h1>
				<p>One last step to activate your profile is to verify your email address</p>
			</div>
		</div>
	</body>
</html>""")

	else:
		validation = False
		check[1] = False


if validation is False:
	error = ""
	for i in range(len(check)):
		if check[i] is False:
			error += checkIndexMeanings[i] + "<br>"
	print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../style.css">
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head>
<body>
<div id="wrapper">
<form name="reg_form" method = "POST" action="/cgi-bin/reg_form.py">
  <div class="container">
    <h1>Register</h1>
    <div id="error">%s</div>
    <p>Please fill in this form to create an account.</p>
    <hr>

  <label for="email"><b>Email</b></label>
  <input type="text" placeholder="Enter Email" name="email" value="%s" required>

  <label for="Username"><b>Username</b></label>
  <input type="text" placeholder="Enter Username" name="user" value="%s" required>

  <label for="psw"><b>Password</b></label>
  <input type="password" placeholder="Enter Password" name="psw" required>

  <label for="psw-repeat"><b>Repeat Password</b></label>
  <input type="password" placeholder="Repeat Password" name="psw-repeat" required>

  <label for="first-name"><b>First name</b></label>
  <input type="text" placeholder="Enter First name" name="name" value="%s" required>

  <label for="last-name"><b>Last name</b></label>
  <input type="text" placeholder="Enter Last name" name="lname" value="%s" required>
"""%(error,email,user,name,lname))
	if(gender == "m"):
		print("""<label for="gender"><b>Gender</b></label><br>
	  <input type="radio" name="gender" value="male" checked="checked"> Male
	  <input type="radio" name="gender" value="female"> Female<br><br>
	""")
	else:	
		print("""<label for="gender"><b>Gender</b></label><br>
	  <input type="radio" name="gender" value="male" > Male
	  <input type="radio" name="gender" value="female" checked="checked"> Female<br><br>
	""")

	print("""<label for="bday"><b>Birthday date</b></label>
  <input type="date" placeholder="Enter Birthday date" name="bday" value="%s">

  <label for="phone"><b>Phone</b></label><br>
    <select name="countryCode" style = "width:150px; heigth:10px">
        <option data-countryCode="GB" value="44" Selected>UK (+44)</option>
        <option data-countryCode="US" value="1">USA (+1)</option>
        <option data-countryCode="BG" value="359">BG (+359)</option>
      <optgroup label="Other countries">
        <option data-countryCode="DZ" value="213">Algeria (+213)</option>
        <option data-countryCode="AD" value="376">Andorra (+376)</option>
        <option data-countryCode="AO" value="244">Angola (+244)</option>
        <option data-countryCode="AI" value="1264">Anguilla (+1264)</option>
        <option data-countryCode="AG" value="1268">Antigua &amp; Barbuda (+1268)</option>
        <option data-countryCode="AR" value="54">Argentina (+54)</option>
        <option data-countryCode="AM" value="374">Armenia (+374)</option>
        <option data-countryCode="AW" value="297">Aruba (+297)</option>
        <option data-countryCode="AU" value="61">Australia (+61)</option>
        <option data-countryCode="AT" value="43">Austria (+43)</option>
        <option data-countryCode="AZ" value="994">Azerbaijan (+994)</option>
        <option data-countryCode="BS" value="1242">Bahamas (+1242)</option>
        <option data-countryCode="BH" value="973">Bahrain (+973)</option>
        <option data-countryCode="BD" value="880">Bangladesh (+880)</option>
        <option data-countryCode="BB" value="1246">Barbados (+1246)</option>
        <option data-countryCode="BY" value="375">Belarus (+375)</option>
        <option data-countryCode="BE" value="32">Belgium (+32)</option>
        <option data-countryCode="BZ" value="501">Belize (+501)</option>
        <option data-countryCode="BJ" value="229">Benin (+229)</option>
        <option data-countryCode="BM" value="1441">Bermuda (+1441)</option>
        <option data-countryCode="BT" value="975">Bhutan (+975)</option>
        <option data-countryCode="BO" value="591">Bolivia (+591)</option>
        <option data-countryCode="BA" value="387">Bosnia Herzegovina (+387)</option>
        <option data-countryCode="BW" value="267">Botswana (+267)</option>
        <option data-countryCode="BR" value="55">Brazil (+55)</option>
        <option data-countryCode="BN" value="673">Brunei (+673)</option>
        <option data-countryCode="BG" value="359">Bulgaria (+359)</option>
        <option data-countryCode="BF" value="226">Burkina Faso (+226)</option>
        <option data-countryCode="BI" value="257">Burundi (+257)</option>
    </optgroup>
  </select>

  (<input type="number" class="tel" pattern="/^-?\\d+\\.?\\d*$/"
  onKeyPress="if(this.value.length==2) return false;" placeholder="88"
  value="%s" name="tel1" min="0" required> ) - 
  <input type="number" class="tel" pattern="/^-?\\d+\\.?\\d*$/"
  onKeyPress="if(this.value.length==3) return false;" placeholder="571"
  value="%s" name="tel2" min="0" required> -
  <input type="number" class="tel" pattern="/^-?\\d+\\.?\\d*$/"
  onKeyPress="if(this.value.length==4) return false;" placeholder="3019"
  value="%s" name="tel3" min="0" required>
  <br>

  <label for="address"><b>Address</b></label>
  <input type="text" placeholder="Enter Address" name="address" value ="%s">

  <label><input type="checkbox" name="terms" required><b>I agree to <a href="https://en.wikipedia.org/wiki/Terms_of_service">Terms of Service</a></b></label><br><br>
  
  <div class="g-recaptcha" data-sitekey="6LclYLoUAAAAAG0FnwojofEbXcmLeE7I3pxv1v51"></div>

    <hr>
    <button type="submit" class="registerbtn">Register</button>
  </div>
  
  <div class="container signin">
    <p>Already have an account? <a href="../login.html">Login</a>.</p>
  </div>
</form>
</div>

</body>
</html>"""%(bday,tel1,tel2,tel3,address))