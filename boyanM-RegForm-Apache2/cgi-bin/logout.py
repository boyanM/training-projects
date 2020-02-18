#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session
import os
from http import cookies

try:
	C = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
	session_id = int(C['session_id'].value)
	
	assert session.deleteSession(session_id) != False, "Error while\
	 deleting session with id:%s"%(session_id)

	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
		 		module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n", mytemplate.render())

except Exception as errors:
	for err in errors:
		logs.adminLog.error(err)
		logs.devLog.error(err)
	print("Content-type:text/html\r\n\r\n")
	print("""Due to heavy load in the site please try to log out again later.
	 We are sorry the problem !""")