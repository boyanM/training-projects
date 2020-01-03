#!/usr/bin/python3

import cgi,cgitb
from callDB import callDB

try:
	form = cgi.FieldStorage()

	basket_id = int(form['basket_id'].value)
	quantity = int(form['quantity'].value)

	db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
	if db.executeDB('update basket set quantity=%s where id=%s;',quantity,basket_id):
		
		price = db.queryDB("""select b.quantity*p.price
		 from products as p,basket as b
		  where b.id=%s and b.product_id =p.id""",basket_id)

		print("Content-type:text/html\r\n\r\n")
		print("Price: ",price[0][0])
	else:
		print()

	customer_id = db.queryDB('select customer_id from basket where id=%s',basket_id)
	total = db.queryDB("""select sum(p.price*b.quantity)
						 from basket as b, products as p
						  where b.product_id = p.id and b.customer_id=%s;""",
						  int(customer_id[0][0]))
	print("|Total:",total[0][0])

except:
	print("Error !")

finally:
	db.closeDB()			
