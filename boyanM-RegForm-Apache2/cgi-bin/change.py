#!/usr/bin/python3

import cgi,cgitb
import psycopg2
from passlib.hash import pbkdf2_sha256

form = cgi.FieldStorage()

email = form["email"].value
psw = form.getvalue('pass')
psw_rep = form.getvalue('pass_rep')


errorMsg = ["Password must be at least 8 characters long","Password and Repeat Password don't match",
"Password must contain at least 1 Capital Letter","Password must contain at least 1 Small-Case Letter"]
check = [True] * 5

if len(psw) < 8: # Length
	check[0] = False

else:
	if psw != psw_rep: # Match
		check[1] = False

	else:
		if not psw.upper().isupper():
			check[2] = False
		else:
			if psw.islower(): #Capital
				check[3] = False

			if psw.isupper(): # Small letter
				check[4] = False

if False in check:
	errors = ""
	for i in range(len(check)):
		if check[i] is False:
			errors += errorMsg[i]+"<br>"

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
<div id="error">%s</div>
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
</html>"""%(errors,link))

else:

	print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>
%s<br>
%s
</body>
</html>"""%("You have succesfully changed your password !",email))


	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
	
		cursor = connection.cursor()
		hash = pbkdf2_sha256.hash(psw)
		psw = hash
		cursor.execute("update customers set password=%s,last_pass_change=%s\
		 where email=%s or username=%s;",(psw,"now()",email,email))
		connection.commit()
		
			
	
	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
		
	finally:
		if connection:
			cursor.close()
			connection.close()

