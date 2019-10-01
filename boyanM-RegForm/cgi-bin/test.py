#!/usr/bin/python3

import cgi,cgitb
import os
ip = cgi.escape(os.environ["REMOTE_ADDR"])
typeip = str(ip)

print("""Content-type:text/html\r\n\r\n
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="../login.css">

</head>
<body>

%s<br>
%s
</body>
</html>
"""%(ip,typeip))