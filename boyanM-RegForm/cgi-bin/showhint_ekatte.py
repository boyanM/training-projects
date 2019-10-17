#!/usr/bin/python3

import psycopg2
import cgi,cgitb
import urllib.parse
import json

form = cgi.FieldStorage()

settlement = form['q'].value
print("""Content-type:text/html\r\n\r\n
<html>""")
try:
	connection = psycopg2.connect(dbname="ekatte",
	user="ekatte_read",
	password="1111",
	host="127.0.0.1",
	port="5432")
		
	cursor = connection.cursor()
	
	cursor.execute("select s.id,s.name,a.name from settlements as s,townships as t,areas as a\
	 where lower(s.name) like concat(lower(%s),%s)\
	 and s.township_id = t.id and t.area_id=a.id limit 5;",(settlement,'%',))
	result = cursor.fetchall()
	print('<datalist id="ekatte">')
	for i in range(len(result)):
		print('<option value="%s">обл. %s</option>'%("[%s] %s"
			%(result[i][0],result[i][1]),result[i][2]))
	print('</datalist>')

except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL:",error)

finally:
	if connection:
		cursor.close()
		connection.close()