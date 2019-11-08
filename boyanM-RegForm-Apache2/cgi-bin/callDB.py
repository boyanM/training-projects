#!/usr/bin/python3
import psycopg2
#Class DB:
	#Methods:
		#-> Open connection to the database callDB(dbname,user,password,host,port) *
		#-> Close connection to the database closeDB() - (like Destructor of the connection)
		#-> Get the cursor getCursorDB()
		#-> Executes queries safely in DB queryDB(query,arg1,...,argN) returns list or None
		#-> Executes inserts and updates safely in DB executeDB(command,arg1,...,argN)
		#-------\ returns True for succesful execute or False for unsuccesfull execute  

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
			print("Error while connection to PostgreSQL:",error)	

	def getCursorDB(self):
		try:
			return self.cursor
		except:
			print("There is no cursor")			

	def closeDB(self):
		try:
			if self.connection:
				self.cursor.close()
				self.connection.close()
		except:
			print('There is no conncetion to close')		

	def queryDB(self,query,*args):
		params = []
		
		for arg in args:
			params.append(arg)
		params = tuple(params)

		try:
			self.cursor.execute(query,params)
			return self.cursor.fetchall()

		except(Exception,psycopg2.Error) as error:
			print("Error executing the query :",error)
			return None


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
			print("Error executing the following:",error)
			return False