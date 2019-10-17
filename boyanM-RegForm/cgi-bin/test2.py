#!/usr/bin/python3

import psycopg2
import cgi,cgitb

str = "[1111] Klaps"

mylist = str.split()
print(type(mylist[0]))
mylist[0] = mylist[0][1:-1]
print(mylist)

l = "[123]"
l = l[1:-1]
print(l)