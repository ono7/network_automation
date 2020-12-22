#!/usr/bin/env python
# this is to alert when a particluar host is on the network doing
# uses smtplib to send sms using a gmail account
# uses scapy module to sniff packets on the wire

import datetime
import time
import smtplib
from scapy.all import *


pcap_filter = r'host 10.255.20.121 and dst port 53'


def send_mail(body):
    try:
        gmail_user = 'xxxxxx@gmail.com'
        gmail_password = 'xxxxx'
        to = ['xxxxxx@mms.att.net']
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, body)
        server.close()
    except Exception as e:
        print e


def schedule():
    hour = datetime.datetime.now().hour
    day = datetime.datetime.today().weekday()
    return day, hour


def check_1():
    day, hour = schedule()
    if (hour >= 8 and hour <= 19) and (day <= 4):
        send_mail('alert $check_1 .121')


def pkt_callback(pkt):
    check_1()


def main():
    sniff(filter=pcap_filter, count=1, prn=pkt_callback)

while True:

    try:
        main()
    except Exception as e:
        print e
    with open('/root/sms.log', 'a') as f:
        f.write(time.strftime('%c') + '\n')
    time.sleep(5400)
