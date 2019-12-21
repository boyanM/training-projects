#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB

form = cgi.FieldStorage()

try: 
	session_id = int(form['session_id'].value)

	check_session = session.isValidSession(session_id)

	if check_session:
		session.renew(session_id)
		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		customer_id = db.queryDB('select customer_id from session where id=%s;',session_id)

		mytemplate = Template(filename='/var/www/test.com/html/templates/main.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",
			mytemplate.render(session_id=session_id,customer_id=int(customer_id[0][0])))

	else:
		session.deleteSession(session_id)
		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))

except:
	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))