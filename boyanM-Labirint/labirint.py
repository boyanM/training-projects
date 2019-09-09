#!/usr/bin/python3


def printMatrix(matrix):
	for cols in labirint:
		for rows in cols:
			print(rows,end=" ")
		print()	


def checkForWall(matrix,currentRow,currentCol,distance):
	position = []
	position.append(distance + 1)
	if matrix[currentRow+1][currentCol] != '*' and currentRow + 1 >= 0 and currentRow+1 < len(matrix[0]):
		position.append(currentRow + 1)
		position.append(currentCol)
		#position.append("right") #direction
		return position

	if matrix[currentRow-1][currentCol] != '*' and currentRow - 1 >= 0 and currentRow - 1 < len(matrix[0]):
		position.append(currentRow - 1)
		position.append(currentCol)
		#position.append("left") #direction
		return position

	if matrix[currentRow][currentCol+1] != '*' and currentCol + 1 >= 0 and currentCol + 1 < len(matrix):
		position.append(currentRow)
		position.append(currentCol + 1)
		#position.append("up") #direction
		return position

	if matrix[currentRow-1][currentCol] != '*' and currentCol - 1 >= 0 and currentCol -1  < len(matrix):
		position.append(currentRow)
		position.append(currentCol - 1)
		#position.append("down") #direction	
		return position

matrix = [
[' ', ' ', ' ', '*', ' ', ' ', ' '],
['*', '*', ' ', '*', ' ', '*', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', '*', '*', '*', '*', '*', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', 'e']
]

currentRow = 0
currentCol = 0
distance = 0
labirint = ""
previous = []


while labirint != 'e':
	position = checkForWall(matrix,currentRow,currentCol,distance,previous)
	previous = position
	print(position)
	currentRow = position[1]
	currentCol = position[2]
	distance = position[0]
	labirint = matrix[position[1]][position[2]]