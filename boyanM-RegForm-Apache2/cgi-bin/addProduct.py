#!/usr/bin/python3

import cgi,cgitb
import psycopg2


form = cgi.FieldStorage()

customer_id = form['customer_id'].value
product_id = form['product_id'].value
print("""Content-type:text/html charset:utf-8\r\n\r\n
<html>
<head>
<meta charset=utf-8>
</head>
""")
try:
	connection = psycopg2.connect(dbname="wordpress",
		user="wpuser",
		password="password",
		host="127.0.0.1",
		port="5432")
	
	cursor = connection.cursor()

	cursor.execute("select price from products where id=%s;",(product_id))
	price = cursor.fetchall()

	cursor.execute("insert into basket (customer_id,product_id,price) values(%s,%s,%s)",
		(int(customer_id),int(product_id),price[0][0]))

	connection.commit()
	print("""<div class="alert success">
	 		 		  <span class="closebtn">&times;</span>  
	 		 		  <strong>Success!</strong> Successfully added product to your basket.
 		 		</div>""")
 

except(Exception,psycopg2.IntegrityError) as err:
 		print("""<div class="alert warning">
  					<span class="closebtn">&times;</span>  
  					<strong>Warning!</strong> Product already in your basket.
				</div>""") 

except(Exception,psycopg2.Error) as error:
		print("""<div class="alert">
 			 		<span class="closebtn">&times;</span>  
  					<strong>Error!</strong> Error while adding product to basket.
				</div>""")

finally:
	if connection:
			cursor.close()
			connection.close()