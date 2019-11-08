#!/usr/bin/python3
import psycopg2
import cgi,cgitb

form = cgi.FieldStorage()
print("Content-type:text/html\r\n\r\n")

email = form["email"].value
reset_token = form["token"].value

print(email,reset_token)

try:
	connection = psycopg2.connect(dbname = 'wordpress',
		user = 'wpuser',
		password = 'password',
		host = '127.0.0.1',
		port = '5432'
		)

	cursor = connection.cursor()
	cursor.execute("select reset_token from customers where email=%s;",((email),))
	result = cursor.fetchone()
	if result[0] == reset_token:
		plusSign = email.find('+')
		if plusSign != -1:
			link = "change.py?email="+ email[:plusSign] + "%2B" + email[plusSign+1:]
		else:
			link = "change.py?email=" + email	
		print("""<html>
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
		print("An error occured please contact site administrator")	

except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL: ",error)

finally:
	if connection:
		cursor.close()
		connection.close()
