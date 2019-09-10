#!/usr/bin/python3

#Style of writing - camelCase
#Author - Boyan M.


import random
import os


def renameFile():#Renames the file from result_*.txt to only result.txt
	directory = os.listdir("/home/boyanm/Documents/Python/Project/Wordpress/")
	for i in directory:
		if i.find("result") != -1 :
		 os.rename(i,"result.txt")
	return	 
		 


def listToString(list):#Coordinates
	command = ""
	count = 0
	for line in list:
		print(count)
		if count != 2500:
			command = command + line + "\n"
			count +=1
		else:
			command = command + line + "\' \\"+"\n"
		
	return command 


def Request(list):#Sends the coordinates to the API
	string = "curl \\" + "\n"
	string += "-X POST \\" + "\n"
	string += "-H 'Content-Type: *' \\" + "\n"
	string += "-d 'recId|prox" + "\n"
	string += listToString(list)
	string += "\'http://batch.geocoder.api.here.com/6.2/jobs?gen=1&app_id=AjegtHqmNoBMUFOvrfUG&app_code=O-TLIg--niEpVNRJ8sD8ug&action=run&mailto=%3Cmy_email%3E&header=true&indelim=%7C&outdelim=%7C&outcols=county%2ClocationLabel%2CdisplayLatitude%2CdisplayLongitude&outputCombined=false&language=en-US&mode=retrieveAddresses\'"
	print(string)

	os.system(string + " -o curl.txt")

	return

def Get(): #Takes the result from the API
	file = open("curl.txt","rt")
	output = file.read()
	file.close()
	find = output.find("<RequestId>")

	requestId = output[slice(find+11,find+42)]



	get = """curl \\
	  -X GET \\
	  -H 'Content-Type: application/octet-stream' \\
	  --get 'https://batch.geocoder.api.here.com/6.2/jobs/"""
	get += requestId
	get +="""/result' \\
	    --data-urlencode 'app_id=AjegtHqmNoBMUFOvrfUG' \\
	    --data-urlencode 'app_code=O-TLIg--niEpVNRJ8sD8ug' --output file.zip
	"""
	os.system(get)
	os.system("unzip -o file.zip")
	return 

def pipeToComma(string):#Changes all Pipes "|" to Commas ","
	count = 0
	while FindSeparator(string,"|") != -1:
		string = string[:FindSeparator(string,"|")] + '"' + "," + string[FindSeparator(string,"|")+1:]
	string = string[:-1] + ",generated" + string[-1:]
	return string	

def Filter(counter):#Transform file to google readable csv
	file = open("result.txt","r")
	lines = file.readlines()
	file.close()

	lines.pop(0)
	
	file = open("markers.csv","a")
	for line in lines:
		newline = str(counter) + "," + line[FindSeparator(line,"|")+1:]
		newline = newline[:FindSeparator(newline,",")+1] +  newline[FindSeparator(newline,",")+5:]
		#Cuts |1|1| ^ row
		newline = pipeToComma(newline)
		file.write(newline)
		counter+=1

	file.close()
	
	return counter


def FindSeparator(string,separator):#Search for specific symbol in a string
	indexOfSeparator = string.find(separator)

	return indexOfSeparator

		
 

def CoordinatesGenerator():
	numberOfCoordinates = 2501
	for i in range(0,numberOfCoordinates,1):
		randomIntLat = random.randint(-90,90)
		randomIntLng = random.randint(-180,180)
	
		listIntLat.append(randomIntLat)
		listIntLng.append(randomIntLng)
	
		randomFloat = random.uniform(0,1)
		randomFloat = round(randomFloat,6)
		if randomFloat not in listFloatLat:
			listFloatLat.append(randomFloat)
	
		randomFloat = random.uniform(0,1)
		randomFloat = round(randomFloat,6)
		if randomFloat not in listFloatLng:
			listFloatLng.append(randomFloat)	
	
		
	
	for var in listIntLng:
		numberLat = float(listIntLat[var]) + listFloatLat[var]
		numberLng = float(listIntLng[var]) + listFloatLng[var]   
		listLat.append(numberLat)
		listLng.append(numberLng)
	
	
	for i in range(numberOfCoordinates):
		line = str(i) + "|" + str(listLat[i]) + "," + str(listLng[i]) + "," + str(0)
		list.append(line)

	return







listIntLat = []
listIntLng = []
listFloatLat = []
listFloatLng = []

listLat = []
listLng = []

list = []

counter = 1

newFile = True

while counter <= 10000:
	if newFile is True:
		newFile = False
		file = open("markers.csv","w")
		file.close()

	else:	
		#CoordinatesGenerator()
	
		#Request(list)
	
		Get()
	
		renameFile()
	
		counter = Filter(counter)







