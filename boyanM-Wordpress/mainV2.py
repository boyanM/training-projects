#!/usr/bin/python3

import requests
import json




def request(count,bbox):
	#Example: ?bbox=22,41,34,43,1000&appid=4d90eceaefb65097f2a3d9f86539e3f5
	url = 'https://api.openweathermap.org/data/2.5/box/city'
	bbox = str(lngBot)+","+str(latBot)+","+str(lngTop)+","+str(latTop)+","+"1000"
	payload = {'bbox':bbox,'appid':'4d90eceaefb65097f2a3d9f86539e3f5'}
	r = requests.get(url,params=payload)
	r_dict = r.json()
	if len(r_dict) == 0:
		neededinfo = [count,'']
		return neededinfo
	else:
		string=''
		listOfAllCities = r_dict['list']
		print(listOfAllCities[0]['name'])
		print(listOfAllCities[0]['id'])
		coordinates_dict = listOfAllCities[0]['coord']
		print(coordinates_dict['Lat'])
		print(coordinates_dict['Lon'])
		#name = name of the city
		#id = id of the city
		#coord = coordinates of the city
	
		for element in range(len(listOfAllCities)):
			coordinates_dict = listOfAllCities[element]['coord']
			coordinates = ''
			coordinates = ","+str(coordinates_dict['Lat']) + "," + str(coordinates_dict['Lon']) + '\n'
			string += str(count) + ","+str(listOfAllCities[element]['id'])
			string +=","+listOfAllCities[element]['name']
			string += coordinates
			count += 1
		neededinfo = []
		neededinfo.append(count)
		neededinfo.append(string)	
		return neededinfo



markers =""
count = 1

#Europe
for lng in range(-9,41,8):
	for lat in range(37,68,3):
		lngBot = lng
		latBot = lat
		lngTop = lng + 8
		latTop = lat + 3
		bbox = str(lngBot) + "," + str(latBot) + "," + str(lngTop) + "," + str(latTop) + ",1000" 
		info = request(count,bbox)
		markers += info[1]
		count = info[0]
		
print(markers)
