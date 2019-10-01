#!/usr/bin/python3

import cgi,cgitb
from passlib.hash import pbkdf2_sha256
import psycopg2
import os
from threading import Timer

def submitBtn():
    print('''<button type="submit" onclick="login.py">Login</button>
   </div>
	<div class="container" style="background-color:#f1f1f1">
    <a class = "acc" href="../index.html">Create account</a></span>
    <a class = "psw" href="#">Forgot password?</a></span>
  </div>
</form>

</body>
</html>''')


def failedLogin(user):
	current_attempt = None
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")

		cursor = connection.cursor()
		cursor.execute("select failed_attemps from customers\
		where (username='%s' or email='%s');"%(user,user))
		counter = cursor.fetchone()
		counter = counter[0]
		counter +=1
		current_attempt = counter

		cursor.execute("update customers set failed_attemps=%i\
		 where username='%s' or email='%s'"%(counter,user,user))
		connection.commit()
	
	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
			if current_attempt != None:
				return current_attempt

def searchInDB(user,psw):
	result = False
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")

		cursor = connection.cursor()


		cursor.execute("select password from customers \
			where (email='%s' or username = '%s');"%(user,user))
		search = cursor.fetchone()
	
		if pbkdf2_sha256.verify(password,search[0]):
			result = True
			cursor.execute("update customers set failed_attemps=0 where username='%s' or email='%s';"%(user,user))
			connection.commit()

	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
		return result

def passwordDelay(user):

	try:	
			wait = 0
			connection = psycopg2.connect(dbname="wordpress",
			user="wpuser",
			password="password",
			host="127.0.0.1",
			port="5432")
			
			cursor = connection.cursor()
			cursor.execute("select failed_attemp_time from customers where (username='%s' or email='%s');"%(user,user))
			lastFail =cursor.fetchone() 
			connection.commit()
			if lastFail[0] != None:
				wait = lastFail[0] + timedelta(seconds = 15)


	except(Exception,psycopg2.Error) as error:
			print("Error while connecting to PostgreSQL:",error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
			if wait != 0:
				return wait

form = cgi.FieldStorage()

user = form.getvalue('uname')

password = form.getvalue('psw')




if searchInDB(user,password) == 1:
		print("""Content-type:text/html\r\n\r\n
<html>
<head>
</head>
	<body>
		<p>Welcome to yout account :)</p>
	</body>
</html>""")
else:
	print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>""")
	attempts = failedLogin(user)
	error = "Invalid Username or Password"
	
	print("""<body>
<div>
<h2>Login Form</h2>
<div id="error">%s</div>
<form action="login.py" method="post">
  <div class="container">
    <label for="uname"><b>Username or E-mail</b></label>
    <input type="text" placeholder="Enter Username" name="uname" value="%s" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>
"""%(error,user))  
    
	if attempts < 5:   
		t = Timer(5.0,submitBtn)
		t.start()
	else:
		t = Timer(300.0,submitBtn)
		t.start()
