#!/usr/bin/python3

import psycopg2
import cgi,cgitb


form = cgi.FieldStorage()

country = form['q'].value

try:
	connection = psycopg2.connect(dbname="wordpress",
	user="wpuser",
	password="password",
	host="127.0.0.1",
	port="5432")
		
	cursor = connection.cursor()
	
	cursor.execute("select country from countries\
	 where lower(country) like concat(lower(%s),lower(%s))",(country,'%'))
	print(cursor.fetchall())
except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL:",error)

finally:
	if connection:
		cursor.close()
		connection.close()