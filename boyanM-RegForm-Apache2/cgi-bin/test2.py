#!/usr/bin/python3

from http import cookies
import cgi,cgitb
C = cookies.SimpleCookie()

print("Content-type:text/html\r\n\r\n")

print(C)