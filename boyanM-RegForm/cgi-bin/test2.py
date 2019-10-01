#!/usr/bin/python3

import datetime
from datetime import timedelta  

import psycopg2


try:
	connection = psycopg2.connect(dbname = 'wordpress',
		user = 'wpuser',
		password = 'password',
		host = '127.0.0.1',
		port = '5432'
		)


	selectRows = ('select * from customers;')


	cursor = connection.cursor()
	cursor.execute('select * from customers')

	customers = cursor.fetchall()
	
	for i in customers:
		print(i)
		for j in range(len(i)):
			print(i[j])
	connection.commit()

	
		
except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL: ",error)

finally:
	if(connection):
		cursor.close()
		connection.close()