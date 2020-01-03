#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB

#=======================================================================
form = cgi.FieldStorage()

session_id = int(form['session_id'].value)

check_session = session.isValidSession(session_id)

if check_session:
	session.renew(session_id)
	db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
	

else:
	session.deleteSession(session_id)
	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
		module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))