#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session

form = cgi.FieldStorage()

try: 
	session_id = int(form['session_id'].value)

	check_session = session.isValidSession(session_id)

	if check_session:
		session.renew(session_id)
		mytemplate = Template(filename='/var/www/test.com/html/templates/main.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(session_id=session_id))

	else:
		session.deleteSession(session_id)
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))

except:
	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))