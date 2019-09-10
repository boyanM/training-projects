#!/usr/bin/python3

#BFS Algorythm

from collections import deque

class Point:
	distance = 0
	def __init__(self,row,col):
		self.row = row
		self.col = col
		 


def move(seen,matrix,path):
	point = Point(0,0) 
	q = deque()
	q.append((point.row,point.col,point.distance))
	seen[point.row][point.col] = True
	while len(q) != 0:
		p = q[0] # TUPLE(p[0] -> row, p[1] -> col, p[2] -> distance)
		if matrix[p[0]][p[1]] != '*':	
			path.append(q[0])
		q.popleft()
		if matrix[p[0]][p[1]] == 'e':
			return p[2]

		#GO DOWN
		if p[0] + 1 >= 0 and p[0] + 1 < len(matrix) and seen[p[0]+1][p[1]] == False:
			q.append((p[0]+1,p[1],p[2]+1))
			seen[p[0]+1][p[1]] = True
			#print("(",p[0],",",p[1],p[2],") => (",p[0]+1,",",p[1],") moved one cell DOWN")

		#GO UP			
		if p[0] - 1 >= 0 and p[0] - 1 < len(matrix) and seen[p[0]-1][p[1]] == False:
			q.append((p[0]-1,p[1],p[2]+1))
			seen[p[0]-1][p[1]] = True
			#print("(",p[0],",",p[1],p[2],") => (",p[0]-1,",",p[1],") moved one cell UP")
			

		#GO RIGHT
		if p[1] + 1 >= 0 and p[1] + 1 < len(matrix[0]) and seen[p[0]][p[1]+1] == False:
			q.append((p[0],p[1]+1,p[2]+1))
			seen[p[0]][p[1]+1] = True
			#print("(",p[0],",",p[1],p[2],") => (",p[0],",",p[1]+1,") moved one cell RIGHT")


		#GO LEFT
		if p[1] - 1 >= 0 and p[1] - 1 < len(matrix[0]) and seen[p[0]][p[1]-1] == False:
			q.append((p[0],p[1]-1,p[2]+1))
			seen[p[0]][p[1]-1] = True
			#print("(",p[0],",",p[1],p[2],") => (",p[0],",",p[1]-1,") moved one cell UP")
	return -1




matrix = [
[' ', ' ', ' ', '*', ' ', ' ', ' '],
['', '', ' ', '*', '*', '*', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
['*', '*', '*', ' ', '', '', ''],
[' ', ' ', ' ', ' ', ' ', ' ', 'e']
]

seen = []
path = deque()

for i in range(len(matrix)):
	row =[]
	for j in range(len(matrix[0])):
		if matrix[i][j] == '*':
			row.append(True)
		else:
			row.append(False)
	seen.append(row)
distance = move(seen,matrix,path)

if distance == -1:
	print("No path to the destination")
else:
	print("The shortest path is: ",distance)	

	last = path[-1]
	for counter in range (distance,-1,-1):
		for i in range(len(path)):
			if path[i][0] + 1 == last[0] or path[i][0] -1 == last[0] or path[i][0] == last[0]:
				check1 = True
			else:
				check1 = False

			#print(path[i][1] + 1," == ",last[1] )
			if path[i][1] + 1 == last[1] or path[i][1] -1 == last[1] or path[i][1] == last[1]:
				check2 = True
			else:
				check2 = False

			if path[i][2] ==  counter and (check1 and check2) and  path[i][2] != last[2]:
				last = path[i]
				matrix[path[i][0]][path[i][1]] = '@'


rowend = ['_','_','_','_','_','_','_']


matrix.insert(0,rowend)
for i in range(len(matrix)):
	matrix[i].insert(0,"|")
	matrix[i].append("|")
matrix.append(rowend)

matrix[0][0] = ""
matrix[-1][-1] = ""

for i in range(len(matrix)):
	for j in range(len(matrix[0])):
		print(matrix[i][j],end=" ")
	print()
						

