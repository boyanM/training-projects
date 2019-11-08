#!/usr/bin/python3

import cgi,cgitb

info = "нг"
info = u' '.join((info, info)).encode('utf-8').strip()

print("""Content-type:text/html\r\n\r\n
	<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8"/>
</head>
<body>
<p>%s</p>
</body>
</html>
"""%info.decode('utf-8'))
