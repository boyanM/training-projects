#!/usr/bin/python3

from http import cookies
import os
from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB

#=======================================================================
try:
	form = cgi.FieldStorage()

	# CHECK SESSION
	total = form['total'].value

	C = cookies.SimpleCookie()
	cookie_string = os.environ.get('HTTP_COOKIE')
	C.load(cookie_string)
	session_id = int(C['session_id'].value)

	#Check Session
	check_session = session.validate(session_id)

	if check_session:
		session.renew(session_id)

		#Form with shipping information
		mytemplate = Template(filename='/var/www/test.com/html/templates/order.txt',
		 		module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(price=total))

	else:
		session.deleteSession(session_id)
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))
except Exception as errors:
	for err in errors:
		logs.adminLog.error(err)
		logs.devLog.error(err)
	
	print("Content-type:text/html\r\n\r\n")
	print("""At the moment this page is unavaible. Please try again later""")
