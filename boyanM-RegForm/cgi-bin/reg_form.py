#!/usr/bin/python3

import cgi,cgitb
import psycopg2
import re

form = cgi.FieldStorage()

email = form.getvalue('email')
match = re.match('^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$',email)


check = [True,True,True,True,True,True]
checkIndexMeaning=["Invalid e-mail"]
if(match == None):
	check[0] = False;

user = form.getvalue('user')

name = form.getvalue('full-name')

gender = form.getvalue('gender')

bday = form.getvalue('bday')

phone = form.getvalue('phone')

address = form.getvalue('address')




if(check[0]):
	print( """Content-type:text/html\r\n\r\n
	<html>
	<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="../reg_form.css">
	</head>
	<body>""")
	print(email)
	print('</body>')
	print('</html>')
else:
	error = ""
	for i in check:
		if i is False:
			error+=checkIndexMeaning[i];
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

  <label for="full-name"><b>Full name</b></label>
  <input type="text" placeholder="Enter Full name" name="full-name" value="%s" required>
"""%(error,email,user,name))
if(gender == "male"):
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
  <input type="text" placeholder="Enter Phone" name="phone" value ="%s">

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

