import os

import smtplib
from email.message import EmailMessage

def send_email():
    msg = EmailMessage()
    msg.set_content("This is an automated email.")
    msg['Subject'] = "Automated Email"
    msg['From'] = os.environ["EMAIL_USER"]
    msg['To'] = os.environ["EMAIL_TO"]

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    smtp.send_message(msg)

send_email()