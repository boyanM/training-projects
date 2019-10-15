#!/usr/bin/python3

import psycopg2
import cgi,cgitb


form = cgi.FieldStorage()

country = form['q'].value


try:
	connection = psycopg2.connect(dbname="wordpress",
	user="wp_read",
	password="1111",
	host="127.0.0.1",
	port="5432")
		
	cursor = connection.cursor()
	
	cursor.execute("select country from countries\
	 where lower(country) like concat(lower(%s),lower(%s)) limit 5",(country,'%'))
	result = cursor.fetchall()
	
	print("""Content-type:text/html\r\n\r\n
<html>""")

	print('<datalist id="countries">')
	for i in range(len(result)):
		print('<option value="%s">'%(result[i][0]))
	print('</datalist>')


except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL:",error)

finally:
	if connection:
		cursor.close()
		connection.close()