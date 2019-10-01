#!/usr/bin/python3

import cgi,cgitb
import psycopg2

print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Customers</title>')
print ('<meta name="viewport" content="width=device-width, initial-scale=1">')
print ('<meta charset="UTF-8">' ) 
print ('</head>')
print ('<body>')

print('<link rel="stylesheet" type="text/css" href="../search.css">')

print ('<h2>Customers</h2>')

try:
	connection = psycopg2.connect(dbname = 'wordpress',
		user = 'wpuser',
		password = 'password',
		host = '127.0.0.1',
		port = '5432'
		)


	selectRows = ('select * from customers;')


	cursor = connection.cursor()

	cursor.execute(selectRows)

	customers = cursor.fetchall()
	colnames = [desc[0] for desc in cursor.description]

	connection.commit()

	
		
except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL: ",error)

finally:
	if(connection):
		cursor.close()
		connection.close()		


print('<table>')
print('<tr>')

for i in range(len(colnames)):
	print('<th>',colnames[i],'</th>')

print('</tr>')
for i in customers:
	print("<tr>")
	for j in range(len(i)):
		print("<td>",i[j],"</td>")
print("</tr>")

print("</table><br><br>")
print ('</body>')
print ('</html>')


