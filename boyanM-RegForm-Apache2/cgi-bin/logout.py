#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session

print("Content-type:text/html\r\n\r\n")
form = cgi.FieldStorage()

session_id = int(form['session_id'].value)

session.deleteSession(session_id)

mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
	 		module_directory='/tmp/mako_modules')
print("Content-type:text/html\r\n\r\n", mytemplate.render())