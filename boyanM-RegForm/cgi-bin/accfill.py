#!/usr/bin/python3

import psycopg2
import json
import cgi,cgitb
import os
print("""Content-type:text/html\r\n\r\n
<html>""")
form = cgi.FieldStorage()

username = form.parse()


print(username)

try:
	connection = psycopg2.connect(dbname="wordpress",
	user="wp_read",
	password="1111",
	host="127.0.0.1",
	port="5432")
		
	cursor = connection.cursor()
	
	#cursor.execute("select cu.username,cu.email,cu.phone,c.country_id,cu.address\
	 #from customers as cu,countries as c where  ")
	#result = cursor.fetchall()
	
	

	#print('<datalist id="countries">')
	#for i in range(len(result)):
		#print('<option value="%s">'%(result[i][0]))
	#print('</datalist>')



except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL:",error)

finally:
	if connection:
		cursor.close()