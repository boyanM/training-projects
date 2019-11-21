#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi,cgitb
import psycopg2
from passlib.hash import pbkdf2_sha256

import os



def newCustomer(user,psw):
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
		
		cursor = connection.cursor()
		hash = pbkdf2_sha256.hash(psw)
		psw = hash

		cursor.execute("insert into admins(username,password)\
		 values (%s,%s)",(user,psw))
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


form = cgi.FieldStorage()

user = form.getvalue('user')

psw = form.getvalue('psw')

conf_psw = form.getvalue('psw-repeat')


check = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
checkIndexMeanings=["Invalid e-mail","Username already in use"
,"The username already exists. Please use a different username",
"Password and Repeat Password don't match", "Username cannot be longer than 30 characters",
"First name cannot be longer than 30 characters","Invalid date",
"Invalid phone number","Address cannot be longer than 30 characters",
"Last name cannot be longer than 30 characters","Password must be at least 8 characters long",
"Password must contain at least 1 Capital Letter",
"Password must contain at least 1 Small-Case Letter","Password must contain letters",
"Please check out the reCAPTCHA","Password cannot contain the username"]

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

			 
validation = True
for i in check:
	if i is False:
		validation = False

if(validation):

	add = newCustomer(user,psw)

	if add is True:
		print("""Content-type:text/html\r\n\r\n
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="https://test.com/login.css">
	</head>
	<body>
		<div id="wrapper">
			<div class="container">
				<h1>Successful Registration</h1>
				<p>You can now login in back-office</p>
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
<html lang="bg">

<head>
<meta charset=utf-8>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="https://test.com/login.css">
</head>
<body>
<div id="wrapper">
<form name="reg_form" method = "POST" action="https://test.com/cgi-bin/admin_reg_form.py">
  <div class="container">
    <h1>Register</h1>
    <div id="error">%s</div>
    <p>Please fill in this form to create an account.</p>
    <hr>

  <label for="Username"><b>Username</b></label>
  <input type="text" placeholder="Enter Username" name="user" value="%s" required>

  <label for="psw"><b>Password</b></label>
  <input type="password" placeholder="Enter Password" name="psw" required>

  <label for="psw-repeat"><b>Repeat Password</b></label>
  <input type="password" placeholder="Repeat Password" name="psw-repeat" required>
  <hr>
    <button type="submit" class="registerbtn">Register</button>
</form>
</div>
 </body>
</html>
"""%(error,user))
	

