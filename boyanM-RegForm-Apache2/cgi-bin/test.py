#!/usr/bin/python3

from http import cookies
import cgi,cgitb
import requests

C['session_id'] = 61
C['session_id']['expires'] = 86400
C['session_id']['path'] = '/'

print(C.output(header="Set-Cookie:"))

print("Content-type:text/html\r\n\r\n")

print("""<form name="quantity_form"
 method = "POST"
  action="https://test.com/cgi-bin/test2.py">
	<label for="Quantity">Quantity</label>
	<input type="number" name="quantity" min="1" value="4" required>
	
	<button type="submit" class="registerbtn">
		Order now !</button>
	</form>""")