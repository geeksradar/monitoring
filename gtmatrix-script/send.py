#! /usr/bin/python3.6
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from datetime import date


# Replace sender@example.com with your "From" address. 
# This address must be verified.
SENDER = 'sender-email'  
SENDERNAME = 'GTmetrix Report'

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT  = 'receiver-email'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "SMTP Username"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "SMTP Password"

# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
CONFIGURATION_SET = "ConfigSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon), 
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
# endpoint in the appropriate region.
HOST = "email-smtp.us-east-1.amazonaws.com"
PORT = 587

today = date.today()
d2 = today.strftime("%B %d, %Y")

# The subject line of the email.
SUBJECT = 'GTmetrix Report - {0} '.format(d2)

def style_line(s):
    '''Rendering odd and even rows with different color'''
    return ['background-color: #D4E6F1' if i%2!=0 else 'background-color: #85C1E9' for i in range(len(s))]

file = "gtmetrix.csv"
df = pd.read_csv(file)
df = pd.DataFrame(df)

htmTable = df.style.apply(style_line).render()

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES Test\r\n"
             "This email was sent through the Amazon SES SMTP "
             "Interface using the Python smtplib package."
            )

# The HTML body of the email.
BODY_HTML = htmTable

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
# Comment or delete the next line if you are not using a configuration set
# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
part2 = MIMEText(BODY_HTML, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)


# Try to send the message.
try:  
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    #stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print ("Error: ", e)
else:
    print ("Email sent!")
