#!/usr/bin/python3

#Code Style - camelCase
#Author - Boyan Milanov

import requests
import json
import psycopg2
import time

def request(count,bbox):
	#Example: ?bbox=22,41,34,43,1000&appid=4d90eceaefb65097f2a3d9f86539e3f5
	url = 'https://api.openweathermap.org/data/2.5/box/city'
	payload = {'bbox':bbox,'appid':'4d90eceaefb65097f2a3d9f86539e3f5'}
	r = requests.get(url,params=payload)
	r_dict = r.json()
	if len(r_dict) == 0:
		return (count,'')
	else:
		string=''
		listOfAllCities = r_dict['list']
		coordinates_dict = listOfAllCities[0]['coord']
		for element in range(len(listOfAllCities)):
			coordinates_dict = listOfAllCities[element]['coord']
			coordinates = ''
			coordinates = ","+str(coordinates_dict['Lat']) + "," + str(coordinates_dict['Lon']) + '\n'
			string += str(count) + ","+str(listOfAllCities[element]['id'])
			string +=","+ "'" + listOfAllCities[element]['name'] + "'"
			string += coordinates
			count += 1
			
		return (count,string)

def geoCalc(lngBot,latBot,lngTop,latTop):
	localArea = []
	if lngBot > lngTop:
		tmp = lngBot
		lngBot = lngTop
		lngTop = tmp
		del tmp

	if latBot > latTop:
		tmp = latBot
		latBot = latTop
		latTop = tmp
		del tmp

	for lng in range(lngBot,lngTop-7,8):
		for lat in range(latBot,latTop-2,3):
			localArea.append((lng,lat,lng+8,lat+3)) #Tuple (Lon Bottom,Lat Bottom, Lon Top, Lat Top)
	return localArea
			
count = 1
markers = ""

area = []

#South America
SA = geoCalc(-71,-17,-50,13)

#Europe
EU = geoCalc(-9,37,47,70)

#Wyoming - U.S.
WY = geoCalc(-111,40,-103,45)

#From Arkansas to New York
A_NY = geoCalc(-93,33,-70,43)

#Asia
AS = geoCalc(8,77,134,46)

area.extend(SA)
area.extend(EU)
area.extend(WY)
area.extend(A_NY)
area.extend(AS)

print("Number of Cities: ",len(area))

start = time.time()
for i in range(len(area)):
	bbox = str(area[i][0]) + "," + str(area[i][1]) + "," + str(area[i][2])
	bbox += "," + str(area[i][3]) + ",1000" 
	info = request(count,bbox)
	count = info[0]
	markers += info[1]
print(markers)
end = time.time()
alltime = end - start
print("Transfer from API time: ",alltime)
start = time.time()

try:
	connection = psycopg2.connect(dbname = "wordpress",
		user = "wpuser",
		password = "password",
		port="5432",
		host="127.0.0.1")
	cursor = connection.cursor()
	cursor.execute("select count(id) from markers; ")
	empty = cursor.fetchone()
	if empty[0] != 0:
		cursor.execute("truncate markers")
	lines = markers.splitlines()
	for i in range(len(lines)):
		insert = "insert into markers(id,number,country,lat,lng) values (" + lines[i] + ");"
		cursor.execute(insert)
		connection.commit()
except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
finally:
	if(connection):
		cursor.close()
		connection.close()
		print("Connection to PostgreSQL is closed")

end = time.time()
alltime = end - start
print("Transfer data to PostgreSQL time : ",alltime)