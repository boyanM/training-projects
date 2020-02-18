#!/usr/bin/python3

from http import cookies
import cgi,cgitb
import logs
from callDB import callDB


def createSession(user):
	try:
		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
		assert db != False
		
		C = cookies.SimpleCookie()
		
		user_id = db.queryDB('''select id 
								from customers 
								where username=%s''',user)
		
		assert user_id != False
		user_id = user_id[0][0]

		session_id = db.addSessionDB('''insert into
		session(customer_id,created,user_timeout)
		values(%s,now(),now() + interval '30 minutes') returning id;''',user_id)

		assert session_id != False

		C['session_id'] = session_id
		C['session_id']['expires'] = 86400
		C['session_id']['path'] = '/'
	
	except:
		logs.adminLog.error("Error while creating the session")
		logs.devLog.exception("Error while creating the session")
		print("There is a huge traffic in the store. Try again later.")


	finally:
		db.closeDB()

def validate(session_id):
	try:
 		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
 		assert db != False

 		check = db.queryDB('''select
 		 					  (select user_timeout from session
 		 					  where id=%s) > now();''',session_id)
 		assert check != False
 		check = check[0][0]

 		if check == True:
 			return True
 		else:
 			return False
	
	except:
		logs.adminLog.error("Error while validating the session of %s"%(session_id))
		logs.devLog.exception("Error while validating the session of %s"%(session_id))
		print("This page is on huge load. Please try again later.")		
		return False

	finally:
		db.closeDB()

def renew(session_id):
	try:
 		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
 		assert db != False		

 		update = db.executeDB('''update session set
 		 user_timeout = now() + interval '30 minutes' where id=%s''',
 		 session_id)

 		assert update != False

	except:
		logs.adminLog.error("Error while renewing the session of user with id: %s"%(session_id))
		logs.devLog.exception("Error while renewing the session of user with id: %s"%(session_id))
		print("Oops we ran into a problem. Please try again later !")		
		return False

	finally:
		db.closeDB()

def deleteSession(session_id):
	try:	
 		db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
 		assert db != False

 		delete = db.executeDB('''delete from session where id=%s''',
 		 session_id)

 		assert delete != False

	except:
		logs.adminLog.error("Error while deleting the session of user with id: %s"%(session_id))
		logs.devLog.exception("Error while deleting the session of user with id: %s"%(session_id))
		print("Sorry we can't log you out now. Please try again in a moment !")
		return False

	finally:
		db.closeDB()