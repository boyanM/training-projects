#!/usr/bin/python3


def spoil(rows,cols,field,row1,col1,row2,col2):
	newfield = []
	for i in range(rows):
		row = []
		for j in range(cols):
			row.append(field[i][j])
		newfield.append(row)

	newfield[row1][col1] = "X"
	newfield[row2][col2] = "X"

	for i in range(rows):
		for j in range(cols):
			if field[i][j] != "O":

				i_copy = i + 1
				if i_copy >= 0 and i_copy < rows:
					newfield[i_copy][j] = "X"
				
				i_copy = i - 1
				if i_copy >= 0 and i_copy < rows :
					newfield[i_copy][j] = "X"

				j_copy = j + 1
				if j_copy >= 0 and j_copy < cols:
					newfield[i][j_copy] = "X"

				j_copy = j - 1
				if j_copy >= 0 and j_copy < cols:
					newfield[i][j_copy] = "X"					



	return newfield

def PrintField(matrix,rows,cols):
	for i in range(rows):
			for j in range(cols):
				print(field[i][j],end=" ")
			print("")
	return





rows,cols,R = input().split()
rows = int(rows) # rows
cols = int(cols) # cols
R = int(R)
field = []
for i in range(rows):
	row = []
	for j in range(cols):
		row.append("O")
	field.append(row)

			 	

row1,col1 = input().split()
row2,col2 = input().split()

row1 = int(row1)
row2 = int(row2)
col1 = int(col1)
col2 = int(col2)

field[row1][col1] = "X"
field[row2][col2] = "X"



for i in range(R):
	field = spoil(rows,cols,field,row1,col1,row2,col2)
count = 0
for i in range(rows):
	for j in range(cols):
		if field[i][j] == "O":
			count+=1
PrintField(field,rows,cols)	
print(count)
