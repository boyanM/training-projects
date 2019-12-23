#!/usr/bin/python3

from callDB import callDB
import session
from datetime import datetime  


if session.isValidSession(44) == True:
	print("True")

else:
	print("False")