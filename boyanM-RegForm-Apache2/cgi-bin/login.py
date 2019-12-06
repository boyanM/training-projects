#!/usr/bin/python3

import cgi,cgitb
from passlib.hash import pbkdf2_sha256
import psycopg2
import os
import datetime
import subprocess
from mako.template import Template


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

		if search == None:
			result = None
		
		else:
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


def failedLogin(user):
	pass_timers = False
	last_login = False
	current_attempt = 0
	
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
		counter = cursor.fetchall()
		
		last_login = counter[0][1]
		if last_login != None:
			current_time = datetime.datetime.now()
			difference_login = current_time - last_login
			difference_login = int(str(difference_login.seconds))
		
		counter = counter[0][0]
		if last_login != None and \
		(difference_login < pass_timers[0][0] or difference_login < pass_timers[0][2]):
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

def loginHTML(user):
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
		 module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=user))

#-------------------------------------------------------------------

form = cgi.FieldStorage()

user = form.getvalue('uname')

password = form.getvalue('psw')

result = validate(user,password)


if result == None:
	loginHTML(user)

else:	
	wait = False
	
	if result != True:
		fail_attempt = failedLogin(user)
		attempts = fail_attempt[0]
		time = (int(fail_attempt[1][0][0]),int(fail_attempt[1][0][1]),int(fail_attempt[1][0][2]))
		failed_login = fail_attempt[2]
	
		if failed_login != None and (result != True or result != -1):
			current_time = datetime.datetime.now()
			difference_login = current_time - failed_login
			difference_login = int(str(difference_login.seconds))
	
			if difference_login < time[0] or difference_login < time[2]:
				wait = True	
	
	
	if result == True and wait != True:
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_suc.txt',
		 module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=user))

	elif result == -1 and wait != True:
		plusSign = user.find('+')
		if plusSign != -1:
			link = "https://test.com/change.py?email="+ user[:plusSign] + "%2B" + user[plusSign+1:]
		else:
			link = "https://test.com/change.py?email=" + user
		
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_change_pass.txt',
		 module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(link=link))
	
	
	else:
		if failed_login != None and attempts < time[1]:   
			if difference_login < time[0]:
				restrict = time[0] - difference_login
				mytemplate = Template(filename='/var/www/test.com/html/templates/login_fail.txt',
		 module_directory='/tmp/mako_modules')
				print("Content-type:text/html\r\n\r\n",
					mytemplate.render(restrict=restrict,user=user))
			else:
				loginHTML(user)
	
		elif failed_login != None and attempts >= time[1]:
			if difference_login < time[2]:
				restrict = time[2] - difference_login
				mytemplate = Template(filename='/var/www/test.com/html/templates/login_fail.txt',
		 module_directory='/tmp/mako_modules')
				print("Content-type:text/html\r\n\r\n",
					mytemplate.render(restrict=restrict,user=user))
			else:
				loginHTML(user)
	
		else:
			loginHTML(user)