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
		
	customer_id = db.queryDB('select customer_id from session where id=%s;',
		session_id)
	basket_info = db.queryDB('''
		select p.name,i.image_url,b.quantity,b.quantity*p.price,b.id
		 from products as p,images as i,basket as b
		  where b.customer_id=%s and b.product_id =p.id and p.image_id=i.id;'''
		  ,customer_id[0][0])

	total = db.queryDB("""select sum(p.price*b.quantity)
						 from basket as b, products as p
						  where b.product_id = p.id and b.customer_id=%s;""",
							customer_id[0][0])

	mytemplate = Template(filename='/var/www/test.com/html/templates/basket.txt',
		module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",
		mytemplate.render(session_id=session_id,
			basket_info=basket_info,total=total[0][0]))

else:
	session.deleteSession(session_id)
	mytemplate = Template(filename='/var/www/test.com/html/templates/login_form.txt',
		module_directory='/tmp/mako_modules')
	print("Content-type:text/html\r\n\r\n",mytemplate.render(user=''))