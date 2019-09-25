#!/usr/bin/python3

import cgi,cgitb
import psycopg2
import re
import datetime
from passlib.hash import pbkdf2_sha256



def uniqueAttribute(attr,value):
	result = -1
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
		
		cursor = connection.cursor()
		if attr == 'e':
			checker = "select count(*) from customers where lower(email) = lower(\'"+value+"\');"
		else:
			checker = "select count(*) from customers where username = \'"+value+"\';"

		cursor.execute(checker)
		result = cursor.fetchall()
		result = int(result[0][0])
		connection.commit()

	except(Exception,psycopg2.Error) as error:
		print("Error while connecting to PostgreSQL:",error)

	finally:
		if connection:
			cursor.close()
			connection.close()
			if result != -1:
				return result

def newCustomer(email,user,psw,name,lname,bday,gender,phone,address):
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
		
		cursor = connection.cursor()
		hash = pbkdf2_sha256.hash(psw)
		psw = hash
		insert = "insert into customers values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(email,user,psw,name,lname,bday,gender,phone,address)
		cursor.execute(insert)
		connection.commit()

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

form = cgi.FieldStorage()

email = form.getvalue('email')
match = re.match('^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$',email)


user = form.getvalue('user')

name = form.getvalue('name')

lname = form.getvalue('lname')

gender = form.getvalue('gender')

bday = form.getvalue('bday')

phone = form.getvalue('phone')

address = form.getvalue('address')

psw = form.getvalue('psw')

conf_psw = form.getvalue('psw-repeat')

check = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
checkIndexMeanings=["Invalid e-mail","There is already a user with this email address"
,"The username already exists. Please use a different username",
"Password and Repeat Password don't match", "Username cannot be longer than 30 characters",
"First name cannot be longer than 30 characters","Invalid date",
"Invalid phone number","Address cannot be longer than 30 characters",
"Last name cannot be longer than 30 characters","Password must be at least 8 characters long",
"Password must contain at least 1 Capital Letter",
"Password must contain at least 1 Small-Case Letter","Password must contain letters"]

if match == None: 
	check[0] = False

if uniqueAttribute('e',email) != 0:
	check[1] = False

if uniqueAttribute('u',user) != 0:
	check[2] = False	

if not lengthCheck(user,30):
	check[4] = False

if not lengthCheck(name,30):
	check[5] = False

if not validateDate(bday):
	check[6] = False

if len(phone) != 12:
	check[7] = False

if not lengthCheck(address,30):
	check[8] = False

if not lengthCheck(lname,30):
	check[9] = False	

if len(psw) < 8:
	check[10] = False

else:
	if psw != conf_psw:
		check[3] = False

	else:
		if not psw.upper().isupper():
			check[13] = False
		else:
			if psw.islower():
				check[11] = False

			if psw.isupper():
				check[12] = False	


if gender == 'male':
	gender = 'm'
else:
	gender = 'f'	






validation = True
for i in check:
	if i is False:
		validation = False

if(validation):
	print( """Content-type:text/html\r\n\r\n
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
	newCustomer(email,user,psw,name,lname,bday,gender,phone,address)
else:
	error = ""
	for i in range(len(check)):
		if check[i] is False:
			error += checkIndexMeanings[i] + "<br>"

	print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../style.css">
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

  <label for="phone"><b>Phone</b></label>
  <input type="number" placeholder="Enter Phone" name="phone" value ="%s">

  <label for="address"><b>Address</b></label>
  <input type="text" placeholder="Enter Address" name="address" value ="%s">

  <label><input type="checkbox" name="terms" required><b>I agree to <a href="https://en.wikipedia.org/wiki/Terms_of_service">Terms of Service</a></b></label>

    <hr>
    <button type="submit" class="registerbtn">Register</button>
  </div>
  
  <div class="container signin">
    <p>Already have an account? <a href="#">Sign in</a>.</p>
  </div>
</form>
</div>

</body>
</html>"""%(bday,phone,address))