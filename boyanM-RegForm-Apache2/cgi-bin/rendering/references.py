#!/usr/bin/python3

from http import cookies
import os
from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB
import logs

#=======================================================================

try:
	form = cgi.FieldStorage()

	C = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])

	session_id = int(C['session_id'].value)
	customer_id = int(C['customer_id'].value)

	check_session = session.validate(session_id)
	if check_session:
		
		assert (session.renew(session_id) != False),"Error while renewing\
		 session of user with id:%s"%(session_id)

		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		assert db != False,"Errow while connecting to the database"

		order_info = db.queryDB("""select c.username,p.name,o.price,o.quantity
		 from orders as o,products as p,customers as c
		  where p.id = o.product_id and c.id = o.customer_id ;""")

		assert order_info != False,"Error while displaying the ordered\
		 item to user with id:%s"%(customer_id)

		mytemplate = Template(filename='/var/www/test.com/html/templates/references.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",
			mytemplate.render(order_info=order_info))


	else:
		assert (session.deleteSession(session_id) != False),"Error while\
		 deleting session with id:%s"%(session_id)

		mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))

except Exception as inst:
	for err in inst.args:
		logs.adminLog.error(err)
		logs.devLog.exception(err)

	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
			module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))