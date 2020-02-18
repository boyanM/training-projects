#!/usr/bin/python3

from http import cookies
import cgi,cgitb
import logs
import requests
import os

print("Content-type: text/plain\n")


C=cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
print(C['customer_id'].value)