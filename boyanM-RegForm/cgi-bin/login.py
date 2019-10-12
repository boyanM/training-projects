#!/usr/bin/python3

import cgi,cgitb
from passlib.hash import pbkdf2_sha256
import psycopg2
import os
from threading import Timer
import datetime


def loginHTML(user):
	html = """Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>
<div>
<h2>Login Form</h2>
<div id="error"><p>
Invalid Username or Password
</p></div>
<form action="login.py" method="post">
  <div class="container">
    <label for="uname"><b>Username or E-mail</b></label>
    <input type="text" placeholder="Enter Username" name="uname" value="%s" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>
    <button type="submit" onclick="login.py">Login</button>
   </div>
	<div class="container" style="background-color:#f1f1f1">
    <a class = "acc" href="../index.html">Create account</a></span>
    <a class = "psw" href="../resetpass.html">Forgot password?</a></span>
  </div>
</form>

</body>
</html>
	"""%(user)
	print(html)


def failedLogin(user):
	current_attempt = False
	pass_timers = False
	last_login = False

	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")

		cursor = connection.cursor()
		
		cursor.execute("select pass_auth1_sec, pass_auth2_min, after_attempts from pass_auth;")
		pass_timers = cursor.fetchall()

		cursor.execute("select failed_attemps,failed_login from customers\
		where (username=%s or email=%s);",(user,user))
		counter = cursor.fetchone()
		last_login = counter[1]
		
		current_time = datetime.datetime.now()
		difference_login = current_time - last_login
		difference_login = int(str(difference_login.seconds))
		
		counter = counter[0]
		print(pass_timers)
		if (difference_login < pass_timers[0][0] or difference_login < pass_timers[0][2])\
		 and last_login != None:
			current_attempt = counter

		else:	
			counter += 1
			cursor.execute("update customers set failed_attemps=%s,failed_login=%s\
			where username=%s or email=%s",(counter,'now()',user,user))
			connection.commit()
			current_attempt = counter
		
		

	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
			return (current_attempt,pass_timers,last_login)

def validate(user,psw):
	result = False
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")

		cursor = connection.cursor()


		cursor.execute("select password,last_pass_change from customers \
			where (email=%s or username = %s);",(user,user))
		search = cursor.fetchone()
		
		cursor.execute("select pass_exp from pass_auth;")
		expire_time = cursor.fetchone()[0]	# In seconds
		if pbkdf2_sha256.verify(psw,search[0]):
			timenow = datetime.datetime.now()
			difference = timenow - search[1]
			difference = int(str(difference.seconds))
			if difference <= expire_time:
				result = True
				cursor.execute("update customers set failed_attemps=0 where username=%s or email=%s;",(user,user))
				connection.commit()
			else:
				result = -1

	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
		return result

form = cgi.FieldStorage()

user = form.getvalue('uname')

password = form.getvalue('psw')

result = validate(user,password)

fail_attempt = failedLogin(user)
attempts = fail_attempt[0]
time = (int(fail_attempt[1][0][0]),int(fail_attempt[1][0][1]),int(fail_attempt[1][0][2]))
failed_login = fail_attempt[2]

current_time = datetime.datetime.now()
difference_login = current_time - failed_login
difference_login = int(str(difference_login.seconds))

wait = False
if difference_login < time[0] or difference_login < time[2]:
	wait = True

if result == True and wait != True:
		print("""Content-type:text/html\r\n\r\n
<html>
<head>
</head>
	<body>
		<p>Welcome to yout account :)</p>
	</body>
</html>""")

elif result == -1 and wait != True:
	plusSign = user.find('+')
	if plusSign != -1:
		link = "change.py?email="+ user[:plusSign] + "%2B" + user[plusSign+1:]
	else:
		link = "change.py?email=" + user
	print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>
<h2>Choose new password</h2>
<form action="%s" method="post">
  <div class="container">
    <label for="pass"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="pass" required>

    <label for="pass_rep"><b> Repeat Password</b></label>
    <input type="password" placeholder="Enter Password" name="pass_rep" required>

    <button type="submit">Send me e-mail</button>
  </div>
  <div class="container" style="background-color:#f1f1f1">
    <a class = "acc" href="../index.html">Create account</a></span>
  </div>
</form>
</body>
</html>"""%(link))

else:
	if attempts != False and attempts < time[1] and failed_login != False:   
		if difference_login < time[0]:
			print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>
<div>
<h2>Login Form</h2>
<div id="error"><p>
Invalid Username or Password<br>
Wait %s seconds till next attempt
</p></div>
<form action="login.py" method="post">
  <div class="container">
    <label for="uname"><b>Username or E-mail</b></label>
    <input type="text" placeholder="Enter Username" name="uname" value="%s" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>
    <button type="submit" onclick="login.py">Login</button>
   </div>
	<div class="container" style="background-color:#f1f1f1">
    <a class = "acc" href="../index.html">Create account</a></span>
    <a class = "psw" href="../resetpass.html">Forgot password?</a></span>
  </div>
</form>

</body>
</html>
"""%(time[0]-difference_login,user))
		else:
			loginHTML(user)	

	elif attempts != False and attempts >= time[1] and failed_login != False:
		if difference_login < time[2]:
			print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>
<div>
<h2>Login Form</h2>
<div id="error"><p>
Invalid Username or Password<br>
Wait %s seconds till next attempt
</p></div>
<form action="login.py" method="post">
  <div class="container">
    <label for="uname"><b>Username or E-mail</b></label>
    <input type="text" placeholder="Enter Username" name="uname" value="%s" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>
    <button type="submit" onclick="login.py">Login</button>
   </div>
	<div class="container" style="background-color:#f1f1f1">
    <a class = "acc" href="../index.html">Create account</a></span>
    <a class = "psw" href="../resetpass.html">Forgot password?</a></span>
  </div>
</form>

</body>
</html>
"""%(time[2] - difference_login,user))
		else:
			loginHTML(user)

	else:
		loginHTML(user)
		