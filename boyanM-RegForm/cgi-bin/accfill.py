#!/usr/bin/python3

import psycopg2
import json
import cgi,cgitb
import os
from callDB import callDB

print("""Content-type:text/html\r\n\r\n
<html>""")

form = cgi.FieldStorage()

user = form['user'].value


db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
cursor = db.getCursorDB()
user_data = db.queryDB('select email,username,country_id,address,phone from customers\
 where username=%s',user)
print('''
	<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
	</head>
	<body>
<link rel="stylesheet" type="text/css" href="../style1.css">
	 ''')

print('<p id="open">Welcome to your account %s</p>'%(user))
print("<br>")
print('<hr>')
print("""
		<label>Username</label>
		<input type="text" name="user" value=%s>
		
		<label>E-mail</label>
		<input type="text" name="mail" value=%s>
		
		<label>Country</label>
		<input type="text" name="country" value=%s>
		
		<label>Address</label>
		<input type="text" name="add" value=%s>
		
		<label>Phone</label>
		<input type="text" name="phone" value=%s>
	"""%(user_data[0][1],user_data[0][0],user_data[0][2],user_data[0][3],user_data[0][4]))

print('<hr>')
print('</body>')
print('</html>')
db.closeDB()

#AJAX for authentitication  !!!!!