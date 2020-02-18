#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
import session
from callDB import callDB
import os
from http import cookies
#=======================================================================
try:
	form = cgi.FieldStorage()

	C = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
	session_id = int(C['session_id'].value)
	customer_id = int(C['customer_id'].value)

	check_session = session.validate(session_id)

	if check_session:
		assert (session.renew(session_id) != False),"Error while renewing\
		 the session with id%s"%(session_id)

		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		assert db != False,"Error while connecting to PostgreSQL"	

		basket_info = db.queryDB('''
			select p.name,i.image_url,b.quantity,b.quantity*p.price,b.id
			 from products as p,images as i,basket as b
			  where b.customer_id=%s and b.product_id =p.id and p.image_id=i.id;'''
			  ,customer_id)

		assert basket_info != False,"Error while executing the\
		 query,which shows basket information for user_id:%s"%(customer_id)

		total = db.queryDB("""select sum(p.price*b.quantity)
							 from basket as b, products as p
							  where b.product_id = p.id and b.customer_id=%s;""",
								customer_id)
		assert total != False,"Error while executing query\
		,showing the total price for user_id:%s"%(customer_id)

		mytemplate = Template(filename='/var/www/test.com/html/templates/basket.txt',
			module_directory='/tmp/mako_modules')
		print("Content-type:text/html\r\n\r\n",
			mytemplate.render(basket_info=basket_info,total=total[0][0]))

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
	print("""Due to heavy load in the site please try to open the basket again later.
	 We are sorry the problem !""")