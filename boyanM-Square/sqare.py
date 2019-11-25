#!/usr/bin/python3

import math
import time

def isValid(length):
	global r
	r = math.trunc(math.sqrt(length) + 0.5)
	if r*r == length:
		return True
	else:
		return False




a = input()
a = int(a)
start = time.time()

count = []
maxLine = 0
for x in range(1,a+1):
	for y in range(x+1,a+1):
		length = x*x + y*y
		r = 0
		if isValid(length):
			count.append(r)
			if maxLine < r:
				maxLine = r


count = set(count)
count = list(count)
print(maxLine,len(count))

stop = time.time()
print(stop - start)