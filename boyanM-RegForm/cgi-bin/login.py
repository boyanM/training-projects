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
    <a class = "psw" href="../resetpass.html">Forgot password?</a></span>
  </div>
</form>

</body>
</html>''')


def failedLogin(user):
	current_attempt = False
	pass_timers = False
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
		
		cursor.execute("select pass_auth1_sec, pass_auth2_min, after_attempts from pass_auth;")
		pass_timers = cursor.fetchall()

	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
	
	finally:
		if connection:
			cursor.close()
			connection.close()
			return (current_attempt,pass_timers)

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
			where (email='%s' or username = '%s');",(user,user))
		search = cursor.fetchone()
		
		cursor.execute("select pass_exp from pass_auth;")
		expire_time = cursor.fetchone()[0]	# In seconds

		timenow = datetime.datetime.now()
		difference = timenow - search[1]
		difference = int(str(difference.seconds))
		if pbkdf2_sha256.verify(password,search[0]):
				if difference <= expire_time:
					result = True
					cursor.execute("update customers set failed_attemps=0 where username='%s' or email='%s';"%(user,user))
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
if result == True:
		print("""Content-type:text/html\r\n\r\n
<html>
<head>
</head>
	<body>
		<p>Welcome to yout account :)</p>
	</body>
</html>""")

elif result == -1:
	plusSign = email.find('+')
	if plusSign != -1:
		link = "change.py?email="+ email[:plusSign] + "%2B" + email[plusSign+1:]
	else:
		link = "change.py?email=" + email
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


	print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>""")
	fail_attempt = failedLogin(user)
	attempts = fail_attempt[0]
	time = fail_attempt[1]
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

	if attempts!= False and attempts < int(time[0][2]):   
		t = Timer(time[0][0],submitBtn)
		t.start()
	elif attempts != False and attempts >= int(time[0][2]):
		t = Timer(time[0][1],submitBtn)
		t.start()
	elif attempts == False:
		submitBtn()
print("""
	</body>
</html>""")