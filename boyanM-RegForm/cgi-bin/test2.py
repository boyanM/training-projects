#!/usr/bin/python3

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "boyan.milanov@yandex.com"
receiver_email = "boyan.milanov@yandex.com"
password = "Parola42"

message = MIMEMultipart("alternative")
message["Subject"] = "Activate your account"
message["From"] = "boyan.milanov@yandex.com"
message["To"] = "boyan.milanov@yandex.com"

# Create the plain-text and HTML version of your message
text = """\
Hi,
Click the link below to activate your account.
---
Note:
If you have not registered on this site do nothing!"""
html = """\
<html>
  <body>
    <p>Hello,<br>
      Click the link below to activate your account.<br>
       <a href="%s">Click here</a> <br>
       Note:<br>
If you have not registered on this site do nothing!
    </p>
  </body>
</html>
"""%(link)

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.yandex.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

