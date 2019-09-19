#!/usr/bin/python3

import psycopg2
import pandas as pd
import time

def connectToPostgres(insert_request_areas,insert_request_townships,insert_request_settlements):
	start = time.time()
	try:
		connection = psycopg2.connect(database = "ekatte",
			user = "ekatte_user",
			password = "Parola42",
			host = "127.0.0.1",
			port = "5432",
			)

		cursor = connection.cursor()
		cursor.execute(insert_request_areas)
		connection.commit()

		cursor.execute(insert_request_townships)
		connection.commit()

		cursor.execute(insert_request_settlements)
		connection.commit()

	

	except (Exception,psycopg2.Error) as error:
		print("Error, while connecting PostgreSQL: ",error)

	finally:
		if(connection):
			cursor.close()
			connection.close()
			print("Connection to PostgreSQL is closed")
	end = time.time()
	print("Time for importing the date: ",end-start)

# Take area from file Ek_obl.xlsx
try:
	areas = pd.read_excel(r'/home/boyanm/Documents/Python/Project/Ekatte/Ek_obl.xlsx')
	
	number = areas['abc'].max()

	insert_request_areas = 'insert into areas values ' 

	for i in range(number):
		line = '(' + '\'' + areas['oblast'][i] + '\'' +  ',' + '\'' + areas['name'][i] + '\'' + ')' + ','
		insert_request_areas += line

	insert_request_areas = insert_request_areas[:-1]

except:
	print("Error while opening the file")

#print(insert_request_areas)


# Take Townships frop Ek_obst.xlsx
try:
	townships = pd.read_excel(r'/home/boyanm/Documents/Python/Project/Ekatte/Ek_obst.xlsx')
	
	number = townships['abc'].max()

	insert_request_townships = 'insert into townships values ' 


	for i in range(number):
		area_id = townships['obstina'][i]
		line = '(' + '\'' + townships['obstina'][i] + '\'' +  ',' + '\''
		line += townships['name'][i] + '\'' + ',' + '\'' + area_id[:3] + '\'' +')' + ','
		insert_request_townships += line

	insert_request_townships = insert_request_townships[:-1]

except:
	print("Error while opening the file")

#print(insert_request_townships)

# Take Settlements from Ek_atte.xlsx

try:
	settlements = pd.read_excel(r'/home/boyanm/Documents/Python/Project/Ekatte/Ek_atte.xlsx')

	number = settlements['abc'].max()
	number = int(number)

	insert_request_settlements = 'insert into settlements values '
	for i in range(1,number+1,1):
		line = '(' + '\'' + str(settlements['ekatte'][i]) + '\'' +  ',' + '\''
		line += settlements['name'][i] + '\'' + ',' + '\''
		line += settlements['obstina'][i] + '\'' + ',' + '\''
		line += settlements['t_v_m'][i] + '\'' + ')' + ','
		insert_request_settlements += line
	insert_request_settlements = insert_request_settlements[:-1]

except:
	print("Error while opening the file")

#print(insert_request_settlements)

connectToPostgres(insert_request_areas,insert_request_townships,insert_request_settlements)
