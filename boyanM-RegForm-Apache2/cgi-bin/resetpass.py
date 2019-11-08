#!/usr/bin/python3

import cgi,cgitb
import psycopg2
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def checkEmailAndUser(email):
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wp_read",
		password="1111",
		host="127.0.0.1",
		port="5432")
	
		cursor = connection.cursor()
		cursor.execute("select email from customers where email=%s or username=%s;",(email,email))
		email = cursor.fetchone()
		if email != None:
			return email[0]
		else:
			return False
			
	
	except (Exception,psycopg2.Error) as error:
		print('Error while connecting to PostgreSQL:',error)
		
	finally:
		if connection:
			cursor.close()
			connection.close()


def sendMail(email,key):
	plusSign = email.find('+')
	if plusSign != -1:
		email = email[:plusSign] + '%2B' + email[plusSign+1:]

	link = 'http://test.com/cgi-bin/changepass.py?email=%s&token=%s'%(email,key)


	sender_email = "boyan.milanov@yandex.com"
	receiver_email = "boyan.milanov@yandex.com" #emal
	password = "Parola42"
	
	message = MIMEMultipart("alternative")
	message["Subject"] = "Activate your account"
	message["From"] = "boyan.milanov@yandex.com"
	message["To"] = "boyan.milanov@yandex.com"
	
	text = """\
	Hi,
	Click the link below to change you password.
	---
	Note:
	If you have not registered on this site do nothing!"""
	html = """\
	<html>
	  <body>
	    <p>Hello,<br>
	      Click the link below to change the password of your account.<br>
	       <a href="%s">Click here</a> <br>
	       Note:<br>
	If you have not registered on this site do nothing!
	    </p>
	   <img src="Hello-Transparent.png" alt="hi"> 
	  </body>
	</html>
	"""%(link)
	
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	
	message.attach(part1)
	message.attach(part2)
	
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(
	        sender_email, receiver_email, message.as_string()
	    )



def generateKey():
	hexals = ['0','1','2','3','4','5','6','7','8','9'\
	,'A','B','C','D','E','F','a','b','c','d','e','f']
	
	length = 32
	key = ""
	for i in range(length):
		key += random.choice(hexals)
	return key

form = cgi.FieldStorage()
email = form.getvalue("uname")


if email != None:
	email = checkEmailAndUser(email)
	if email != False:
		key = generateKey()
		try:
			connection = psycopg2.connect(dbname="wordpress",
			user="wpuser",
			password="password",
			host="127.0.0.1",
			port="5432")
	
			cursor = connection.cursor()
			cursor.execute("update customers set reset_token=%s where email=%s",(key,email))
			connection.commit()
				
	
		except (Exception,psycopg2.Error) as error:
			print('Error while connecting to PostgreSQL:',error)
			
		finally:
			if connection:
				cursor.close()
				connection.close()
		sendMail(email,key)



		print('Content-Type: text/html\r\n\r\n')
		print('Location: %s'%("../sendmail.html"))
		
		#print(# HTTP says you have to have a blank line between headers and content)
		print('<html>')
		print('<head>')
		print('<meta http-equiv="refresh" content="0;url=%s" />'%("../sendmail.html"))
		print('<title>You are going to be redirected</title>')
		print('</head>')
		print('</html>')
	else:
		print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">
								
</head>
<body>
<div id="error">%s</div>

<h2>Reset Password</h2>
								
<form action="resetpass.py" method="post">
  <div class="container">
    <label for="uname"><b>Username or E-mail</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>
								
    <button type="submit">Send me e-mail</button>
  </div>
								
  <div class="container" style="background-color:#f1f1f1">
    <a class = "acc" href="index.html">Create account</a></span>
  </div>
</form>
</body>
</html>"""%("Invalid E-mail or Username"))
		