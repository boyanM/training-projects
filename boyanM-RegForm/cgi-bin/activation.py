#!/usr/bin/python3
import psycopg2
import cgi,cgitb

form = cgi.FieldStorage()
print("Content-type: text/plain\n")

email = form["email"].value
conf_token = form["token"].value


try:
	connection = psycopg2.connect(dbname = 'wordpress',
		user = 'wpuser',
		password = 'password',
		host = '127.0.0.1',
		port = '5432'
		)

	cursor = connection.cursor()
	cursor.execute("select conf_token from customers where email ='%s';"%(email))
	result = cursor.fetchone()
	if result[0] == conf_token:
		print("Your account is now activated")
		cursor.execute("update customers set confirmed = true where email ='%s';"%(email))
		connection.commit()
	else:
		print("An error occured please contact site administrator")	
except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL: ",error)

finally:
	if connection:
		cursor.close()
		connection.close()

