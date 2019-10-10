#!/usr/bin/python3

import psycopg2
import datetime
from passlib.hash import pbkdf2_sha256

#timenow = datetime.datetime.now()
#
#
#
#try:
#	connection = psycopg2.connect(dbname="wordpress",
#	user="wpuser",
#	password="password",
#	host="127.0.0.1",
#	port="5432")
#
#	cursor = connection.cursor()
#
#
#	cursor.execute("select last_pass_change from customers where id=18;")
#	search = cursor.fetchone()[0]
#	print(type(search))
#	result = timenow - search
#	print(int(str(result.seconds)))
#
#except (Exception,psycopg2.Error) as error:
#	print('Error while connecting to PostgreSQL:',error)
#	
#finally:
#	if connection:
#		cursor.close()
#		connection.close()
#

result = False
try:
	connection = psycopg2.connect(dbname="wordpress",
	user="wpuser",
	password="password",
	host="127.0.0.1",
	port="5432")

	cursor = connection.cursor()

	user='boyan1044@gmail.com'
	password = '123qweASD'
	cursor.execute("select password,last_pass_change from customers \
		where (email='%s' or username = '%s');"%(user,user))
	search = cursor.fetchone()
	
	cursor.execute("select pass_exp from pass_auth;")
	expire_time = cursor.fetchone()[0]	# In seconds

	timenow = datetime.datetime.now()
	difference = timenow - search[1]
	difference = int(str(difference.seconds))
	result = search
	if pbkdf2_sha256.verify(password,search[0]):
			if difference <= expire_time:
				result = True
				cursor.execute("update customers set failed_attemps=0 where username='%s' or email='%s';",(user,user))
				connection.commit()
			else:
				result = -1
	print(result)
except (Exception,psycopg2.Error) as error:
	print('Error while connecting to PostgreSQL:',error)
	
finally:
	if connection:
		cursor.close()
		connection.close()
