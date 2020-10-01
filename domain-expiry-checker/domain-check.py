import datetime
import whois
import json
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import smtplib
import os
from email.mime.text import MIMEText

today = datetime.datetime.today()

def report_via_email():
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_HOST_USER = "AKIAVFU6SDQFVFI2RPHL"
    EMAIL_HOST_PASSWORD = "BGLWjbV+a01GTi+R0ITS5UpoZ4ACo/sOe48VclprvtUf"
    EMAIL_PORT = 587
 
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Domain is about to expire"
    msg['From'] = "friends@botbakery.io"
    msg['To'] = "prateek@botbakery.io"
 
    mime_text = MIMEText("{0} will expire in {1} days".format(i, y))
    msg.attach(mime_text)
 
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail("prateek@botbakery.io","prateek@botbakery.io", msg.as_string())
    s.quit()

with open("sites.json") as sites:
    data  = json.loads(sites.read())
    
    for i in data['sites']:
        dom = whois.whois(i)
        exp = dom.expiration_date
        dt_exp = exp - today
        x = dt_exp.days
        y = int(x)
        print(y)
        if y < 220:
            report_via_email()