#!/usr/bin/python3


def inputCheck(number):
	if number <= 0 or number >= 100000:
		num = -1
		while True:
			if num <= int(0) or num >= int(100000):
				print("Please enter value between 0 and 100000")
				num = input()
				num = int(num)
			else:
				return num	
		
	else:
		return number
	


line = input()
line = int(line)
line = inputCheck(line)

a = input()
a = int(a)
a = inputCheck(a)


b = input()
b = int(b)
b = inputCheck(b)

c = input()
c = int(c)
c = inputCheck(c)

georgeLoop = (line / a) + 1
georgeLoop = int(georgeLoop)
gerganaLoop = (line / b) + 1
gerganaLoop = int(gerganaLoop)

georgeArray = [None] * georgeLoop
gerganaArray = [None] * gerganaLoop


georgeArray[0] = 0
for i in range(1,georgeLoop):
	georgeArray[i] = georgeArray[i-1] + a

gerganaArray[0] = line
for i in range(1,gerganaLoop):
	gerganaArray[i]=gerganaArray[i-1] -b	

lineCopy = line +1
lineArray = [None]*lineCopy

for i in range(georgeLoop):
	for j in range(gerganaLoop):
		result = abs(georgeArray[i] - gerganaArray[j])
		if result == c:
			if georgeArray[i] > gerganaArray[j]:
				for var in range(gerganaArray[j],georgeArray[i]+1):
					lineArray[var] = "RED"
			else:
				for var in range(georgeArray[i],gerganaArray[j]+1):
					lineArray[var] = "RED"



result = 0
lenghtOfArray = len(lineArray) -1



for i in range(0,lenghtOfArray):
	if lineArray[i] == 'RED' and lineArray[i+1] == None:
		result+=1
	if lineArray[i] == None and lineArray[i+1] == 'RED':
		result+=1
	if lineArray[i] == None and lineArray[i+1] == None:
		result+=1

print(result)			

