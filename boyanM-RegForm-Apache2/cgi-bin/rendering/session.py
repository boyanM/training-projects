#!/usr/bin/python3

import psycopg2
import cgi,cgitb
from datetime import datetime  
from datetime import timedelta  
from callDB import callDB

def createSession(user_id):
	try:
		site_db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		timeout = site_db.queryDB('select user_timeout,auto_logout from pass_auth;')
		user_timeout = datetime.now() + timedelta(seconds=timeout[0][0])
		auto_logout = datetime.now() + timedelta(seconds=timeout[0][1])
		
		user_timeout = user_timeout.strftime("%Y-%m-%d %H:%M:%S")
		auto_logout = auto_logout.strftime("%Y-%m-%d %H:%M:%S")


		check = site_db.executeDB('''insert into
		 session(customer_id,timestamp,user_timeout,auto_logout)
		 values(%s,%s,to_timestamp(%s,\'YYYY-MM-DD HH24:MI:SS\'),
			(select to_timestamp(%s,\'YYYY-MM-DD HH24:MI:SS\')))''',
			user_id,'now()',user_timeout,auto_logout)
		
		session_id = site_db.queryDB("""select id from session
								 	where customer_id = %s
								 	 and auto_logout = %s""",user_id,auto_logout)

		return session_id[0][0]

	except (Exception,psycopg2.Error) as error:
		print("Error while creating session:",error)
		return False

	finally:
		site_db.closeDB()
	

def renew(session_id):
	try:
		site_db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		timeout = site_db.queryDB('select user_timeout from pass_auth;')

		user_timeout = datetime.now() + timedelta(seconds=timeout[0][0])

		user_timeout = user_timeout.strftime("%Y-%m-%d %H:%M:%S")

		site_db.executeDB('''update session set user_timeout = %s
		 where id = %s;''',user_timeout,session_id)

		return session_id

	except (Exception,psycopg2.Error) as error:
		print("Error while creating session:",error)
		return False

	finally:
		site_db.closeDB()

def isValidSession(session_id):
	try:
		site_db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		timeout = site_db.queryDB('select user_timeout from session;')

		if datetime.now() >= timeout[0][0]:
			return False

		else:
			return True

	except (Exception,psycopg2.Error) as error:
		print("Error while checking the session:",error)
		return False