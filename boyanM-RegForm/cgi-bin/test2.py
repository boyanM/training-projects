#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi,cgitb
import json
from callDB import callDB

wp_db = callDB('ekatte','ekatte_read','1111','127.0.0.1','5432')

users = wp_db.queryDB('select name from settlements where id =6')
print(users)
user = users[0][0]

info = user

print("""Content-type:text/html\r\n\r\n
	<html>
	<head>
        <meta charset="UTF-8">
    </head>
    %s
"""%info)
