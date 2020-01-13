#!/usr/bin/python3

from http import cookies
import os
import cgi,cgitb
import requests

C = cookies.SimpleCookie()

print("Content-type:text/html\r\n\r\n")

cookie_string = os.environ.get('HTTP_COOKIE')

C.load(cookie_string)
session = int(C['session_id'].value)

print(session)