#!/usr/bin/python3

import psycopg2
import cgi,cgitb

try:
	connection = psycopg2.connect(dbname="wordpress",
	user="wpuser",
	password="password",
	host="127.0.0.1",
	port="5432")

	cursor = connection.cursor()
		
	cursor.execute("select failed_attemps,failed_login from customers\
		where (username='boyan' or email='boyan10');")
	p = cursor.fetchall()

	print(p)

except (Exception,psycopg2.Error) as error:
	print('Error while connecting to PostgreSQL:',error)
	
finally:
	if connection:
		cursor.close()
		connection.close()
