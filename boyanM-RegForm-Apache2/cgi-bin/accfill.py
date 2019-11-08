#!/usr/bin/python3

import psycopg2
import json
import cgi,cgitb
import os
from callDB import callDB
from passlib.hash import pbkdf2_sha256

print("""Content-type:text/html\r\n\r\n

<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="http://test.com/main.css">
	</head>
	<body>
	<ul>
	  <li><a class="active" href="http://test.com/php/check.php?goto=main.php">Home</a></li>
	  <li>
	  	<a href="http://test.com/php/check.php?goto=cgi-bin/accfill.py?acc=<?php echo $_SESSION['user'] ?>">Account</a>
	  </li>
	  <li><a href="#contact">Contact</a></li>
	  <li><a href="#about">About</a></li>
	</ul>

	""")

	
form = cgi.FieldStorage()

user = form['acc'].value

username = form.getvalue('username')
password = form.getvalue('psw')
password_repeat = form.getvalue('psw_repeat')
mail = form.getvalue('mail')
country = form.getvalue('country')
address = form.getvalue('address')
phone = form.getvalue('phone')


wp_db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
user_data = wp_db.queryDB('select cu.username,cu.email,c.country,cu.address,cu.phone\
 from customers as cu,countries as c\
 where username=%s and cu.country_id=c.id;',user)

wp_db.closeDB()

ekatte_db = callDB('ekatte','ekatte_read','1111','127.0.0.1','5432')
ekatte_data = ekatte_db.queryDB('select id,name from settlements where id=%s;',user_data[0][3])
ekatte_db.closeDB()

if username == None and password == None and password_repeat == None and mail == None \
and country == None and address == None and phone == None:
	
	#address = "[%s] "%(ekatte_data[0][0])
	#address += ekatte_data[0][1]
	address = "[1] a" 

	print('''
	<link rel="stylesheet" type="text/css" href="../style1.css">
	<script type="text/javascript" src="http://test.com/js/editacc.js"></script>
	<script type="text/javascript" src="http://test.com/js/showhint.js"></script>
	
		 ''')
	
	print('<p id="open">Welcome to your account %s</p>'%(user))
	print("<br>")
	print('<hr>')
	print("""
			<form name="edit_acc" method="POST"
			 action="http://test.com/cgi-bin/accfill.py?acc=%s">
			<label>Username</label>
			<input type="text" class="acc_field" name="username" value=%s disabled required>
			
			<label>Password</label>
			<input type="password" class="acc_field" id="psw" name="psw" disabled>
			 	
			 	<div id="message">
				  <h3>Password must contain the following:</h3>
				  <p id="letter" class="invalid">A <b>lowercase</b> letter</p>
				  <p id="capital" class="invalid">A <b>capital (uppercase)</b> letter</p>
				  <p id="number" class="invalid">A <b>number</b></p>
				  <p id="length" class="invalid">Minimum <b>8 characters</b></p>
				</div>
	
			<label id="psw_repeat_label">Repeat Password</label>
			<input type="password" class="acc_field" id="psw_repeat" name="psw_repeat" disabled>
	
			<label>E-mail</label>
			<input type="text" class="acc_field" name="mail" value=%s disabled required>
			
			<label for="Country">Country</label>
	  		<input type="text" onkeyup="showHint(this.value)" value=%s name="country"
	  		 id="txtHint" class="acc_field" list="countries" disabled required>
	
			<label for="address">Address</label>
	  		<input type="text" onkeyup="hint(this.value)" name="address"
	  		 id="ekatteHint" class="acc_field" list="ekatte" value=%s disabled required>
	
			<label>Phone</label>
			<input type="text" class="acc_field" name="phone" value=%s disabled required>
		"""%(user,user_data[0][0],user_data[0][1],
			user_data[0][2],address,user_data[0][4]))
	
	print('<hr>')
	
	print('<button type="button" id="edit" onclick="editAcc()">Edit profile</button>')
	print('<input type="submit" id="save_btn" value="Save">')
	print('</form>')
	print('</body>')
	print('</html>')



elif username == user_data[0][0] and password == None and mail == user_data[0][1]\
			and country == user_data[0][2] and address == ekatte_data[0][0]\
			and phone ==user_data[0][4]:
	
	#address = "[%s] "%(ekatte_data[0][0])
	#address += str(ekatte_data[0][1])
	address = "[1] a"

	print('''
	<link rel="stylesheet" type="text/css" href="../style1.css">
	<script type="text/javascript" src="http://test.com/js/editacc.js"></script>
	<script type="text/javascript" src="http://test.com/js/showhint.js"></script>
	
		 ''')
	
	print('<p id="open">Welcome to your account %s</p>'%(username))
	print("<br>")
	print('<hr>')
	print("""
			<form name="edit_acc" method="POST" 
			 action="http://test.com/cgi-bin/accfill.py?acc=%s">
			<label>Username</label>
			<input type="text" class="acc_field" name="username" value=%s disabled required>
			
			<label>Password</label>
			<input type="password" class="acc_field" id="psw" name="psw" disabled>
			 	
			 	<div id="message">
				  <h3>Password must contain the following:</h3>
				  <p id="letter" class="invalid">A <b>lowercase</b> letter</p>
				  <p id="capital" class="invalid">A <b>capital (uppercase)</b> letter</p>
				  <p id="number" class="invalid">A <b>number</b></p>
				  <p id="length" class="invalid">Minimum <b>8 characters</b></p>
				</div>
	
			<label id="psw_repeat_label">Repeat Password</label>
			<input type="password" class="acc_field" id="psw_repeat" name="psw_repeat" disabled>
	
			<label>E-mail</label>
			<input type="text" class="acc_field" name="mail" value=%s disabled required>
			
			<label for="Country">Country</label>
	  		<input type="text" onkeyup="showHint(this.value)" value=%s name="country"
	  		 id="txtHint" class="acc_field" list="countries" disabled required>
	
			<label for="address">Address</label>
	  		<input type="text" onkeyup="hint(this.value)" name="address"
	  		 id="ekatteHint" class="acc_field"list="ekatte" value=%s disabled required>
	
			<label>Phone</label>
			<input type="text" class="acc_field" name="phone" value=%s disabled required>
		"""%(username,user_data[0][0],user_data[0][1],user_data[0][2],address,user_data[0][4]))
	
	print('<hr>')
	
	print('<button type="button" id="edit" onclick="editAcc()">Edit profile</button>')
	print('<input type="submit" id="save_btn" value="Save">')
	print('</form>')
	print('</body>')
	print('</html>')

else:
	#print(username,password,password_repeat,mail,country,address,phone)
	
	new_add = address.split()
	new_add = new_add[0][1:-1]
	address = "[1] a"


	wp_db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
	country_id = wp_db.queryDB('select id from countries where country=%s',country)
	country_id = country_id[0][0]
	wp_db.executeDB('update customers set username=%s,\
		email=%s,country_id=%s,address=%s,phone=%s;',
		username,mail,country_id,new_add,phone)
	
	if password != None:
		hash = pbkdf2_sha256.hash(password)
		new_pass = hash
		wp_db.executeDB('update customers set password=%s',new_pass)
	
	wp_db.closeDB()
	
	print('''
	<link rel="stylesheet" type="text/css" href="../style1.css">
	<script type="text/javascript" src="http://test.com/js/editacc.js"></script>
	<script type="text/javascript" src="http://test.com/js/showhint.js"></script>
	''')
	
	print('<p id="open">Welcome %s</p>'%(username))
	print("<br>")
	print('<hr>')
	print("""
			<form name="edit_acc" method="POST" 
			 action="http://test.com/cgi-bin/accfill.py?acc=%s">
			<label>Username</label>
			<input type="text" class="acc_field" name="username" value=%s disabled required>
			
			<label>Password</label>
			<input type="password" class="acc_field" id="psw" name="psw" disabled>
			 	
			 	<div id="message">
				  <h3>Password must contain the following:</h3>
				  <p id="letter" class="invalid">A <b>lowercase</b> letter</p>
				  <p id="capital" class="invalid">A <b>capital (uppercase)</b> letter</p>
				  <p id="number" class="invalid">A <b>number</b></p>
				  <p id="length" class="invalid">Minimum <b>8 characters</b></p>
				</div>
	
			<label id="psw_repeat_label">Repeat Password</label>
			<input type="password" class="acc_field" id="psw_repeat" name="psw_repeat" disabled>
	
			<label>E-mail</label>
			<input type="text" class="acc_field" name="mail" value=%s disabled required>
			
			<label for="Country">Country</label>
	  		<input type="text" onkeyup="showHint(this.value)" value=%s name="country"
	  		 id="txtHint" class="acc_field" list="countries" disabled required>
	
			<label for="address">Address</label>
	  		<input type="text" onkeyup="hint(this.value)" name="address"
	  		 id="ekatteHint" class="acc_field"list="ekatte" value=%s disabled required>
	
			<label>Phone</label>
			<input type="text" class="acc_field" name="phone" value=%s disabled required>
		"""%(username,username,user_data[0][1],user_data[0][2],address,user_data[0][4]))
	
	print('<hr>')
	
	print('<button type="button" id="edit" onclick="editAcc()">Edit profile</button>')
	print('<input type="submit" id="save_btn" value="Save">')
	print('</form>')
	print('</body>')
	print('</html>')

	print('<hr>')


	print('</body>')
	print('</html>')
