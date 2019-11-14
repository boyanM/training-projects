#!/usr/bin/python3
import cgi,cgitb
from passlib.hash import pbkdf2_sha256
import psycopg2
import datetime
from callDB import callDB

form = cgi.FieldStorage()

user = form.getvalue('username')
password = form.getvalue('psw')
password_repeat = form.getvalue('psw_repeat')
mail = form.getvalue('mail')
country = form.getvalue('country')
phone = form.getvalue('phone')

wp_db = callDB('wordpress','wpuser','password','127.0.0.1','5432')

user_data = wp_db.queryDB('select cu.username,cu.email,c.country,cu.phone\
 from customers as cu,countries as c\
 where username=%s and cu.country_id=c.id;',user)

error = ""

#if user != user_data[0][0]:
#	change = wp_db.executeDB('update customers set username=%s\
#		 where username=%s;',user,user_data[0][0])
#	if change == False:
#			error += "The username already exists. Please use a different username. <br>"

if password != None:
	if password == password_repeat:
		hash = pbkdf2_sha256.hash(password)
		new_pass = hash
		wp_db.executeDB('update customers set password=%s\
			where username=%s',new_pass,user)
	else:
		error += "Password and Repeat password don't match ! <br>"	
	
if mail != user_data[0][1]:
	change = wp_db.executeDB('update customers set email=%s\
		where email=%s',mail,user_data[0][1])
	if change == False:
		error += "The email already exists. Please use a different email <br>"

if country != user_data[0][2]:
	country_id = wp_db.queryDB('select id from countries where country=%s',country)
	country_id = country_id[0][0]
	wp_db.executeDB('update customers set country_id=%s\
		where username=%s',country_id,user)

if phone !=user_data[0][3]:
		wp_db.executeDB('update customers set phone=%s\
		 where username=%s',phone,user)
	
wp_db.closeDB()

if(error != ""):
	print('''
Content-type:text/html\r\n\r\n

<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="http://test.com/main.css">
	</head>
	<body>
		%s
	</body>
</html>
		'''%(error))

else:
	print('''
Content-type:text/html\r\n\r\n

<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="http://test.com/main.css">
	</head>
	<body>
		Succesfull update
	</body>
</html>
		''')			





