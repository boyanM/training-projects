#!/usr/bin/python3

import math
from collections import deque


class Path:
	def __init__(self,position,distance):
		self.position = position
		self.distance = distance

	def printPath(self):
		print("position = ",self.position)
		print("distance = ",self.distance)	




def isIntersect(circleA,circleB):
	distanceA_B = math.sqrt((circleA[1] - circleB[1])**2 + (circleA[2] - circleB[2])**2)
	#print("circleA = ",circleA[0],"circleB = ",circleB[0],"distanceA_B = ",distanceA_B,"check1 = ",(circleA[3] + circleB[3]),"check2 = ",abs(circleA[3]-circleB[3]))
	if distanceA_B < (circleA[3] + circleB[3]) and distanceA_B > abs(circleA[3]-circleB[3]):
		return True	
	else:
		return False




def shortest_path(graph,seen,last):
	queue = deque()

	start = Path("A1",0)
	queue.append(start)
	
	for i in range(len(graph)):
		for j in range(len(seen[i])):
			if seen[i][j] == start.position:
				seen[i][j] = True
	currentPosition = queue[0]
	while len(queue) != 0:
		currentPosition = queue[0]
		#currentPosition.printPath()
		queue.popleft()
	
		distance = currentPosition.distance
		currentNumber = int(currentPosition.position[-1])-1
		
		if currentPosition.position == last:
			return distance
	
		for i in range(len(graph[currentNumber])):
			if seen[currentNumber][i] != True:
				#print("List index => ",i)
				queue.append(Path(graph[currentNumber][i],distance+1))
				seen[currentNumber][i] = True
	return -1			

n = int(input())
circles = []

for i in range(n):
	name = "A" + str(i+1)
	xCoord,yCoord,radius = input().split()
	xCoord = int(xCoord)
	yCoord = int(yCoord)
	radius = int(radius)
	if xCoord < 10000 and xCoord > -10000 and yCoord < 10000 and yCoord > -10000 and radius < 10000 and radius > 0:
		print(name,xCoord,yCoord,radius)
		circles.append((name,xCoord,yCoord,radius)) 


#circle1 = ("A1",0,0,4)
#circle2 = ("A2",8,0,5)
#circle3 = ("A3",16,0,5)
#circle4 = ("A4",22,10,8)
#circle5 = ("A5",22,-8,8)
#circle6 = ("A6",30,2,6)



#circles.append(circle1)
#circles.append(circle2)
#circles.append(circle3)
#circles.append(circle4)
#circles.append(circle5)
#circles.append(circle6)


graph = []
for i in range(len(circles)):
	graph.append([])
	for j in range(len(circles)):
		if i != j:
			if isIntersect(circles[i],circles[j]):
				graph[i].append(circles[j][0])

print(graph)


#FIFI
seen = graph.copy()
last = "A" + str(n)
result = shortest_path(graph,seen,last)
print(type(result))
if result != -1:
	print("Shortest path is: ",result)
else:
	print("No path to the destination!")	


"""
6
0 0 4
8 0 5
16 0 5
22 1 8
22 -8 8
30 2 6


4
0 0 1
2 1 3
5 4 3
6 5 1

"""

