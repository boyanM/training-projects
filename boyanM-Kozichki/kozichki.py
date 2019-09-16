#!/usr/bin/python3

import sys

def findRev(index,goats):
	for i in range(len(goats)-1,-1,-1):
		if goats[i] == index:
			return i

def optimal(courses,mass,goats):
	goats_copy = list(goats)
	order = []
	for i in range(courses):
		SUM = mass
		for j in reversed(goats_copy):
			if j != "X" and SUM - j >= 0:
				index = findRev(j,goats_copy)
				goats_copy[index] = "X"
				SUM -= j
				order.append(j)
	return (goats_copy,order)


# 4,8,15,16,23,42
# 666,42,7,13,400,511,600,200,202,111,313,94,280,72,42

#goats = [23,34,45,23,21,12]
goats = [666000,42000,7000,13000,400000,511000,600000,200000,202000,111000,313000,94000,280000,72000,42000]
numberOfGoats,courses =input().split()
numberOfGoats = int(numberOfGoats)
courses = int(courses)

validation1 = numberOfGoats >= 1 and numberOfGoats <= 1000
validation2 = courses >= 1 and courses <= 1000 
print(validation1)

#for i in range(numberOfGoats):
#	element = int(input())
#	goats.append(element)
#	if element < 1 and element > 100000:
#		print("Enter number between")
#		sys.exit("Invalid input")	

goats.sort()
print(goats)
allMass = sum(goats)
avrMass = int(allMass / courses)

avr_copy = avrMass

check = True

while check:
	result = optimal(courses,avr_copy,goats)
	check2 = True
	for item in result[0]:
		if item != "X":
			check2 = False
	if check2 == False:		
		avr_copy+=1
	else:
		print(avr_copy)
		print(result[1])
		check = False	





			
