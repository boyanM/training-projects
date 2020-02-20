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
		
		basket = db.queryDB("""select """)

		confirm = db.executeDB("""insert into
		 orders(customer_id,price,quantity,product_id)
		  select b.customer_id,b.quantity*p.price,b.quantity,b.product_id 
		  from basket as b,products as p
		   where b.customer_id =%s and  b.product_id=p.id;""",customer_id)

		assert confirm != False,"Error while confirming order\
		 of user with id:%s"%(customer_id)

		delete_basket = db.executeDB("""delete from basket
		  where customer_id=%s""",customer_id)

		assert delete_basket != False,"Error while deleting already\
		 purchased items from the basket of user with id:%s"%(customer_id)

		mytemplate = Template(filename='/var/www/test.com/html/templates/succ.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",mytemplate.render())		

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
