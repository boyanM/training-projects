#!/usr/bin/python3

from mako.template import Template
import cgi,cgitb
from session import session


mytemplate = Template(filename='/var/www/test.com/html/templates/main.txt',
	module_directory='/tmp/mako_modules')
print("Content-type:text/html\r\n\r\n",mytemplate.render())
