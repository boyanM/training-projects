#!/usr/bin/python3

import cgi,cgitb
import psycopg2


form = cgi.FieldStorage()
pass_auth1_sec = form.getvalue('pass_time')
pass_auth2_min = form.getvalue('pass_block')
pass_numOfAttem = form.getvalue('numOfAttempts')
expire_months = form.getvalue('months')

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
password_timers = False

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

	cursor.execute("select pass_auth1_sec, pass_auth2_min, after_attempts,pass_exp from pass_auth;")
	password_timers = cursor.fetchall()
	if pass_auth1_sec != password_timers[0][0] or pass_auth2_min != password_timers[0][1]\
	 or pass_numOfAttem != password_timers[0][2] or expire_months != password_timers[0][3]:
		cursor.execute("update pass_auth set\
		 pass_auth1_sec=%s,pass_auth2_min=%s,after_attempts=%s,pass_exp=%s;"
			,(pass_auth1_sec,pass_auth2_min,pass_numOfAttem,expire_months))
		cursor.execute("select pass_auth1_sec, pass_auth2_min, after_attempts,pass_exp from pass_auth;")
		password_timers = cursor.fetchall()	
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

if(password_timers != False):

	print("""
		<p><strong>Information for password authentication</strong></p>
		<hr>
	<form name="password_timers" method = "POST" action="search.py">
		<label for="Password_timer"><b>After Wrong Attempt Time(Sec)</b></label>
    	<input type="number" placeholder="Please enter time " name="pass_time" value="%s" required><br><br>
		<label for="Password_timer_afterFive"><b>After Five Wrong Attempts Time(Sec)</b></label>
    	<input type="number" placeholder="Please enter time " name="pass_block" value="%s" required><br><br>
    	<label for="number_attem"><b>After how many attempts to trigger the big counter</b></label>
    	<input type="number" placeholder="Please enter number of attempts" name="numOfAttempts" value="%s" required><br><br>
    	<hr>
    	<label for="number_attem"><b>Password expires after (seconds)</b></label>
    	<input type="number" placeholder="Please enter seconds" name="months" value="%s" required>
    	<hr>
    	<button type="submit" class="registerbtn">Save</button>
	"""%(password_timers[0][0],password_timers[0][1],password_timers[0][2],password_timers[0][3]))

print ('</body>')
print ('</html>')


