#!/usr/bin/python3

import cgi,cgitb
import psycopg2

print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Search for a settlement</title>')
print ('<meta name="viewport" content="width=device-width, initial-scale=1">')
print ('<meta charset="UTF-8">' ) 
print ('</head>')
print ('<body>')

print('<link rel="stylesheet" type="text/css" href="../search.css">')

print ('<h2>Search for a settlement</h2>')

print('<form name="serach"  method="POSt" accept-charset="utf-8" action = "/cgi-bin/search.py">')
print('<input name="settlement" type="text" id="myInput"  placeholder="Search for names.." title="Type in a name"/>')
print('</form>')

form = cgi.FieldStorage()
keyword = form.getvalue('settlement')
try:
	connection = psycopg2.connect(dbname = 'ekatte',
		user = 'ekatte_read',
		password = '1111',
		host = '127.0.0.1',
		port = '5432'
		)


	queryForNumberOfRows = ('select'\
							'(select count(*) from settlements) as rows_settlement,'\
							'(select count(*) from townships) as rows_townhips,'\
							'(select count(*) from areas) as rows_areas;')


	cursor = connection.cursor()

	cursor.execute(queryForNumberOfRows)

	NumberOfRowsInTables = cursor.fetchall()

	cursor.execute("select distinct	ty.t_v_m as t_v_m,\
	 s.name as name,t.name as township, a.name as area\
	 	from settlements as s,townships as t,areas as a,types as ty\
	 		where LOWER(s.name) LIKE concat(LOWER(%s),%s)\
	 		 and t.id=s.township_id and t.area_id = a.id and ty.id = s.t_v_m;",(keyword,'%'))


	ListOfMatches = cursor.fetchall()
	connection.commit()


except (Exception,psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL: ",error)

finally:
	if(connection):
		cursor.close()
		connection.close()		


print ("""<table>
  <tr>
    <th>Rows of Settlements Table</th>
    <th>Rows of Townships Table</th>
    <th>Rows of Area Table</th>
  </tr>""")

print("<tr>")
print("<td>",NumberOfRowsInTables[0][0],"</td>")
print("<td>",NumberOfRowsInTables[0][1],"</td>")
print("<td>",NumberOfRowsInTables[0][2],"</td>")
print("</tr></table><br><br>")



print("""<table>
  <tr>
    <th>Type</th>
    <th>Name</th>
    <th>Township</th>
    <th>Area</th>
  </tr>
	""")

counter = 0
for line in ListOfMatches:
	counter +=1
	print("<tr>")
	print("<td>",line[0],"</td>")
	print("<td>",line[1],"</td>")
	print("<td>",line[2],"</td>")
	print("<td>",line[3],"</td>")
	print("</tr>")
print("</tr></table><br><br>")
print("<p>","There is(are) ",counter," row(s) with that match the given expression","</p>")

print ('</body>')
print ('</html>')