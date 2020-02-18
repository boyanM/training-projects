#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB
from http import cookies
import os

form = cgi.FieldStorage()
try: 
	C = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])

	session_id = int(C['session_id'].value)
	customer_id = int(C['customer_id'].value)

	check_session = session.validate(session_id)

	if check_session:
		
		assert (session.renew(session_id) != False),"Error while renewing\
		 session of user with id:%s"%(session_id)
		
		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		assert db != False,"Errow while connecting to the database"

		customer_id = db.queryDB('select customer_id from session where id=%s;',session_id)

		if customer_id != False:
			C['customer_id'] = customer_id[0][0]
			mytemplate = Template(
			filename='/var/www/test.com/html/templates/main.txt',
			module_directory='/tmp/mako_modules'
			)
			print("Content-type:text/html\r\n\r\n",
				mytemplate.render(customer_id=customer_id))
		
		else:
			raise Exception("No session assosiated with that username")

	else:
		assert (session.deleteSession(session_id) != False),"Error while\
		 deleting session with id:%s"%(session_id)

		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))

except Exception as inst:
	for err in inst.args:
		logs.adminLog.error(err)
		logs.devLog.error(err)

	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))