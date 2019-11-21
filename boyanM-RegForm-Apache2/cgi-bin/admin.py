#!/usr/bin/python3

import cgi,cgitb
from passlib.hash import pbkdf2_sha256
import psycopg2
import os
import datetime
import subprocess

def validate(user,psw):
	result = False
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")

		cursor = connection.cursor()
		cursor.execute("select password from admins\
			where username = %s;",(user,))
		search = cursor.fetchone()

		if search == None:
			result = None
		
		else:
			if pbkdf2_sha256.verify(psw,search[0]):
				result = True
			else:
				result = False

	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
		return result


def loginHTML(user):
	html = """Content-type:text/html\r\n\r\n
<html lang="bg">
<head>
<meta charset=utf-8>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>
<div>
<h2>Admin Panel</h2>
<div id="error">
<p>Invalid Username</p></div>
<form action="admin.py" method="post">
  <div class="container">
    <label for="uname"><b>Username or E-mail</b></label>
    <input type="text" placeholder="Enter Username" name="uname" value="%s" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>
    <button type="submit" onclick="admin.py">Login</button>
   </div>
</form>
</body>
</html>
	"""%(user)
	print(html)

form = cgi.FieldStorage()

user = form.getvalue('uname')

password = form.getvalue('psw')

result = validate(user,password)

if result == True:
	print("Content-type:text/html\r\n\r\n")
	redirectURL = "https://test.com/php/startAdminSess.php?user=%s"%(user)

	print('<html>')
	print('<head>')
	print('    <meta http-equiv="refresh" content="0;url='+str(redirectURL)+'" />')
	print('</head>')
	print('</html>')

else:
	loginHTML(user)
