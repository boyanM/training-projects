#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging
import cgi,cgitb
import psycopg2
import re
import datetime
from passlib.hash import pbkdf2_sha256
import requests
import json
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from mako.template import Template

def reCAPTCHA(g_response):
	url = 'https://www.google.com/recaptcha/api/siteverify'
	payload = {'secret' :'6LclYLoUAAAAAH9eix2giVphRCUAj0I9me0azjkz','response':g_response}

	try:
		r = requests.get(url,params=payload)
		r_dict = r.json()
		status = r_dict['success']
		
		if status == False:
			return False
		else:
			return True
	except:
		return False

def newCustomer(email,user,psw,name,lname,bday,gender,phone,address,key,country):
	try:
		connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
		
		cursor = connection.cursor()
		hash = pbkdf2_sha256.hash(psw)
		psw = hash

		add_list = address.split()
		add_list[0] = add_list[0][1:-1]

		cursor.execute("insert into customers\
		 (email,username,password,name,lname,bday,gender,phone,\
		address,conf_token,last_pass_change,country_id)\
		values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,(select id from countries\
		where lower(country)=lower(%s)))"\
		,(email,user,psw,name,lname,bday,gender,phone,int(add_list[0]),key,"now()",country))
		connection.commit()
		return True

	except(Exception,psycopg2.IntegrityError) as err:
		return err
		
	except(Exception,psycopg2.Error) as error:
		print("Error while connecting to PostgreSQL:",error)

	finally:
		if connection:
			cursor.close()
			connection.close()

def lengthCheck(attr,max):
	if len(attr) <= max:
		return True
	else:
		return False

def validateDate(date):

	index = date.find('-')
	year = date[-4:]
	year = int(year)
	currentyear = str(datetime.date.today())
	index = currentyear.find('-')
	currentyear = currentyear[:index]
	currentyear = int(currentyear)
	if year >= currentyear - 100 and year <= currentyear:
		return True
	else:
		return False 

def validatePhone(tel1,tel2,tel3):
	if len(str(tel1)) == 2 and len(str(tel2)) == 3 and len(str(tel3)) == 4:
		return True
	else:
		return False	

def generateKey():
	hexals = ['0','1','2','3','4','5','6','7','8','9'\
	,'A','B','C','D','E','F','a','b','c','d','e','f']
	
	length = 32
	key = ""
	for i in range(length):
		key += random.choice(hexals)
	return key
	

def sendMail(email,key): 
	link = 'http://test.com/cgi-bin/activation.py?email=%s&token=%s'%(email,key)


	sender_email = "boyan.milanov@yandex.com"
	receiver_email = "boyan.milanov@yandex.com" #emal
	password = "Parola42"
	
	message = MIMEMultipart("alternative")
	message["Subject"] = "Activate your account"
	message["From"] = "boyan.milanov@yandex.com"
	message["To"] = "boyan.milanov@yandex.com"
	
	text = """\
	Hi,
	Click the link below to activate your account.
	---
	Note:
	If you have not registered on this site do nothing!"""
	html = """\
	<html>
	  <body>
	    <p>Hello,<br>
	      Click the link below to activate your account.<br>
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


#----------------------------------------------------------------------------
form = cgi.FieldStorage()

email = form.getvalue('email')
match = re.match('^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$',email)


user = form.getvalue('user')

name = form.getvalue('name')

lname = form.getvalue('lname')

gender = form.getvalue('gender')

bday = form.getvalue('birthday')

code = form.getvalue('countryCode')
tel1 = form.getvalue('tel1')
tel2 = form.getvalue('tel2')
tel3 = form.getvalue('tel3')
phone = str(code) + str(tel1)+ str(tel2)+str(tel3)


address = form.getvalue('address')

psw = form.getvalue('psw')

conf_psw = form.getvalue('psw-repeat')

g_response = form.getvalue('g-recaptcha-response')

country = form.getvalue('Country')

error = []
if match == None: 
	error.append("Invalid e-mail")

if not lengthCheck(user,30):
	error.append("Username cannot be longer than 30 characters")

if not lengthCheck(name,30):
	error.append("Username cannot be longer than 30 characters")
	
if not validateDate(bday):
	error.append("Invalid date")

if not lengthCheck(address,30):
	error.append("Address cannot be longer than 30 characters")

if not lengthCheck(lname,30):
	error.append("Last name cannot be longer than 30 characters")

if not validatePhone(tel1,tel2,tel3):
	error.append("Invalid phone number")

if len(psw) < 8:
	error.append("Password must be at least 8 characters long")

else:
	if psw != conf_psw:
		error.append("Password and Repeat Password don't match")

	else:
		if psw.find(user) != -1:
			error.append("Password cannot contain the username")
		else:	
			if not psw.upper().isupper():
				error.append("Password must contain letters")
			else:
				if psw.islower():
					error.append("Password must contain at least 1 Capital Letter")

				if psw.isupper():
					error.append("Password must contain at least 1 Small-Case Letter")

if g_response == None:
		error.append("Please check out the reCAPTCHA")

else:	
	if reCAPTCHA(g_response) is False:
		error.append("Please check out the reCAPTCHA")

if gender == 'male':
	gender = 'm'
else:
	gender = 'f'	


validation = True
if len(error) != 0:
		validation = False
add = ""
if(validation):

	key = generateKey()
	add = newCustomer(email,user,psw,name,lname,bday,gender,phone,address,key,country)
	if add is True:
		plusSign = email.find('+')
		if plusSign != -1:
			newMail = email[:plusSign] + '%2B' + email[plusSign+1:]
			sendMail(newMail,key)
		else:
			sendMail(email,key)

		mytemplate = Template(filename='/var/www/test.com/html/templates/reg_form_suc.txt',
		 module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render())

	else:
		validation = False
		error.append("E-mail or username already in use")

if validation is False:

	mytemplate = Template(filename='/var/www/test.com/html/templates/reg_form_fail.txt',
		 module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(
		add=add,error=error,email=email
		,user=user,name=name,lname=lname
		,gender=gender,bday=bday,tel1=tel1
		,tel2=tel2,tel3=tel3,country=country)
	)