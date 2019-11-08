#!/usr/bin/python3

import cgi,cgitb
import psycopg2


form = cgi.FieldStorage()
pass_auth1_sec = form.getvalue('pass_time')
pass_auth2_min = form.getvalue('pass_block')
pass_numOfAttem = form.getvalue('numOfAttempts')
expire_months = form.getvalue('months')
timeout = form.getvalue('timeout')

print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>Customers</title>')
print('<meta name="viewport" content="width=device-width, initial-scale=1">')
print('<meta charset="UTF-8">' ) 
print('</head>')
print('<body>')
print('<link rel="stylesheet" type="text/css" href="../search.css">')
print('<script type="text/javascript" src="http://127.0.0.1/js/show_content.js"></script>')
print('''<p><strong>Customers</strong>
 <button id="btn_cust1" onclick="showButton('customers','btn_cust1','btn_cust2')"><span>&#8595;</span></button>
 <button id="btn_cust2" onclick="hideButton('customers','btn_cust1','btn_cust2')"><span>&#8593;</span></button></p>''')
print('<div id="customers">')
timers = False

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

	#cursor.execute("select pass_auth1_sec, pass_auth2_min, after_attempts,pass_exp,user_timeout from pass_auth;")
	cursor.execute("select * from pass_auth;")
	
	timers = cursor.fetchall()
	print(timers)
	if None not in timers[0] and pass_auth1_sec != None and timeout != None:
		if int(pass_auth1_sec) != timers[0][0] or int(pass_auth2_min) != timers[0][1]\
		 or int(pass_numOfAttem) != timers[0][2] or int(expire_months) != timers[0][3]\
		  or int(timeout) != timers[0][4]:
			cursor.execute("update pass_auth set\
			 pass_auth1_sec=%s,pass_auth2_min=%s,after_attempts=%s,pass_exp=%s,user_timeout=%s;"
				,(pass_auth1_sec,pass_auth2_min,pass_numOfAttem,expire_months,timeout))
			connection.commit()
			cursor.execute("select * from pass_auth;")
			timers = cursor.fetchall()
			
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
print('</div>')

print('''<p>
		<strong>Information for password authentication</strong>
 		<button id="btn_timer1" onclick="showButton('timer','btn_timer1','btn_timer2')"><span>&#8595;</span></button>
 		<button id="btn_timer2" onclick="hideButton('timer','btn_timer1','btn_timer2')"><span>&#8593;</span></button>
		</p>''')

print('<div id="timer">')

if(timers != False):

	print("""
		<hr>
	<form name="timers" method = "POST" action="search.py">
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
		</div>"""%(timers[0][0],timers[0][1],timers[0][2],timers[0][3]))
 		

print('''<p>
		<strong>User Timeout</strong>
 		<button id="btn_timeout1" type="button" onclick="showButton('user_timeout','btn_timeout1','btn_timeout2')"><span>&#8595;</span></button>
 		<button id="btn_timeout2" type="button" onclick="hideButton('user_timeout','btn_timeout1','btn_timeout2')"><span>&#8593;</span></button>
		</p>''')
print("""
	<div id="user_timeout">
		<hr>
		<label for="User Timeout"><b>User Timeouts after N(Sec)</b></label>
    	<input type="number" placeholder="Please enter time " name="timeout" value="%s" required><br><br>
    	<hr>
	</div>"""%(timers[0][4]))

print("""<button type="submit">Save</button>
    </form>""")

print ('</body>')
print ('</html>')


