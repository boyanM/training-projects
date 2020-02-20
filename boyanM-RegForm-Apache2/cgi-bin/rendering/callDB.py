#!/usr/bin/python3
import psycopg2
import logs

#Class DB:
	#Methods:
		#-> Open connection to the database callDB(dbname,user,password,host,port) *
		#-> Close connection to the database closeDB() - (like Destructor of the connection)
		#-> Get the cursor getCursorDB()
		#-> Executes queries safely in DB queryDB(query,arg1,...,argN) returns list or None
		#-> Executes inserts or updates safely in DB executeDB(command,arg1,...,argN)
		#-------\ returns True for successful execute or False for unsuccessful execute  

class callDB:
	def __init__(self,dbname,user,password,host,port):
		try:
			self.connection = psycopg2.connect(dbname=dbname,
				user=user,
				password=password,
				host=host,
				port=port
				)
			
			self.cursor = self.connection.cursor()
		
		except (Exception,psycopg2.Error) as error:
			logs.adminLog.error("Error while connection to PostgreSQL")
			logs.devLog.exception("Error while connection to PostgreSQL")
			return False

	def getCursorDB(self):
		try:
			return self.cursor
		except:
			logs.adminLog.error("There is no cursor to return")
			logs.devLog.exception("There is no cursor to return")

	def closeDB(self):
		try:
			if self.connection:
				self.cursor.close()
				self.connection.close()
		except:
			logs.adminLog.error("There is no connection to close")
			logs.devLog.exception("There is no connection to close")

	def queryDB(self,query,*args):
		params = []
		
		for arg in args:
			params.append(arg)
		params = tuple(params)

		try:
			self.cursor.execute(query,params)
			return self.cursor.fetchall()

		except(Exception,psycopg2.Error) as error:
			logs.adminLog.error("Error while executing the query")
			logs.devLog.exception("Error while executing the query")
			return False


	#command -> Insert or Update
	def executeDB(self,command,*args):
		params = []
		
		for arg in args:
			params.append(arg)
		params = tuple(params)

		try:
			self.cursor.execute(command,params)
			self.connection.commit()
			return True

		except(Exception,psycopg2.Error) as error:
			logs.adminLog.error("Error while executing insert or update in DB")
			logs.devLog.exception("Error while executing insert or update in DB")			
			return False

	def addSessionDB(self,command,*args):
		params = []
		
		for arg in args:
			params.append(arg)
		params = tuple(params)

		try:
			self.cursor.execute(command,params)
			self.connection.commit()
			return self.cursor.fetchall()[0][0]

		except(Exception,psycopg2.Error) as error:
			logs.adminLog.error("Error while adding session in DB")
			logs.devLog.exception("Error while adding session in DB")			
			return False			