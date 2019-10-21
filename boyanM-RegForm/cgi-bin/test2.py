#!/usr/bin/python3

import psycopg2
from callDB import callDB



db = callDB('wordpress','wpuser','password','127.0.0.1','5432')
db.closeDB()

cursor =db.getCursorDB()
cursor.execute("select username from customers where username='boyan10';")



check = db.queryDB("select id from customers where username=%s",'boyan10')
#check = db.executeDB("update customers set email=%s where username=%s",'boyan1044@gmail.com','boyan10')
print(check)
