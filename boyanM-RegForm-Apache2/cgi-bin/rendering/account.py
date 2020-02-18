#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB
from passlib.hash import pbkdf2_sha256
import os
from http import cookies


#==================================================================================
try:
	form = cgi.FieldStorage()
	
	C = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
	session_id = int(C['session_id'].value)

	if session.validate(session_id):
		assert (session.renew(session_id) != False),"Error while renewing\
		 the session with id%s"%(session_id)

		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		assert db != False,"Error while connecting to PostgreSQL"

		user_info = db.queryDB('''select
		 cu.username,cu.email,s.name,cu.phone,c.country
		  from customers as cu,settlements as s,countries as c
		   where cu.id = (select customer_id from session where id =%s)
	         and cu.address=s.id and cu.country_id=c.id;''',session_id)
	    # output from the query -> username,email,address name,phone,country name
		
		assert user_info != False,"Error while executing the query\
		,showing the user information"

		username = user_info[0][0]
		email = user_info[0][1]
		address = user_info[0][2]
		phone = user_info[0][3]
		country = user_info[0][4]

		change = {}

		customer_username = form.getvalue('username')
		customer_email = form.getvalue('email')
		customer_address = form.getvalue('address')
		customer_country = form.getvalue('country')
		customer_phone = form.getvalue('phone')

		if customer_username != None and username != customer_username:
			change['username'] = customer_username

		if customer_email != None and email != customer_email:
			change['email'] = customer_email
		
		if customer_address != None and address != customer_address:
			if customer_country == 'Bulgaria':
				address_id = form.getvalue('address')
				address_id = address_id[address_id.find('[')+1:address_id.find(']')]
				address_id = int(address_id)
				change['address'] = address_id
			
			else:
				change['address'] = 0


		if customer_phone != None and phone != customer_phone:
			change['phone'] = int(form.getvalue('phone'))

		if customer_country != None and country != customer_country:
			country_id = db.queryDB('select id from countries where country=%s',
				form.getvalue('country'))
			change['country_id'] = int(country_id[0][0])	

		if form.getvalue('psw') != None and form.getvalue('psw') == form.getvalue('psw_repeat'):
			password = str(form.getvalue('psw'))
			hash = pbkdf2_sha256.hash(password)
			change['password'] = hash

		if len(change) != 0:
			update = ""
			for key in change:
				if key == 'phone' or key == 'country' or key =='address':
					update = key + "=" + str(change[key])	+ ","
				else:	
					update= key + "='" + str(change[key])	+ "',"
			update = update[:-1]
			update = "update customers set " + update + " where username=%s"

			check = db.executeDB(update,username)
			assert check != False,"Error while changing\
			 information for %s"%(change['username'])

			mytemplate = Template(filename='/var/www/test.com/html/templates/account.txt',
				module_directory='/tmp/mako_modules')
			print("Content-type:text/html\r\n\r\n",
				mytemplate.render(username = customer_username,
				 email = customer_email,country=customer_country,
				 address = customer_address, phone = customer_phone))

		else:	
			mytemplate = Template(filename='/var/www/test.com/html/templates/account.txt',
		 		module_directory='/tmp/mako_modules')
			print("Content-type:text/html\r\n\r\n",
				mytemplate.render(username = username, email = email,
					country = country,address=address , phone = phone))

	else:
		assert session.deleteSession(session_id) != False,"Error while deleting\
		 the session of %s"%(change['username'])
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))

except Exception as errors:
	for err in errors:
		logs.adminLog.error(err)
		logs.devLog.error(err)