#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
client SSID beacon recon

used to monitor night activity around the house from untrusted wifi clients.

requires nic in monitor mode using aircrack-ng/iwconfig + scapy and decent wifi nic to monitor for frames.

maintains client database and trusted SSID list used to ignore clients looking for local APs (neighbors etc)

'''
import smtplib
import time
import sqlite3
from scapy.all import *


# known and trusted SSIDs
trusted_ssid = [
        ]
client_white_list = []

# init client db
client_db = {}

# client sqlite db
sqlite3_db = '/home/jlima/rogue_wifi_beacons.db'

def send_mail(body):
    try:
        gmail_user = ''
        gmail_password = ''
        to = ['']
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, body)
        server.close()
    except Exception as e:
        print(e)

def check_client_db(client, ssid, arrival_time):
    header = '\n\n' + arrival_time + '\n'
    if not client in client_db:
        client_db[client] = [ssid]
        body = header + 'new: ' + client + ' -> ssid: ' + ssid
        send_mail(body)
        print('{}: new: {} -> ssid: {}'.format(arrival_time,client,ssid))
    elif client in client_db and ssid not in client_db[client]:
        client_db[client].append(ssid)
        body = header + 'update: ' + client + ' ssids: ' + str(client_db[client])
        send_mail(body)
        print('{}: update: {} -> ssids: {}'.format(arrival_time,client, client_db[client]))

def client_db_insert(db, client, ssid, arrival_time, day_of_week):
    try:
        ssid.encode('ascii') # temp testing non ascci ssid
        db.execute('INSERT INTO clients VALUES (?,?,?,?)', (day_of_week, arrival_time, \
            client, ssid ))
        db.commit()
    except UnicodeEncodeError:
        print('non ascii ssid\n')
        pass
    except Exception as e:
#        print(e)
        pass

def pkt_handler(pkt):
    if pkt.haslayer(Dot11):
        try:
            if '\x00' in pkt.info or pkt.addr2 in client_white_list:
                pass
            elif pkt.info not in trusted_ssid and len(pkt.info) > 0:
                arrival_time = datetime.fromtimestamp(pkt.time).strftime('%Y-%m-%d %H:%M:%S')
                day_of_week = datetime.fromtimestamp(pkt.time).strftime('%a')
                check_client_db(pkt.addr2, pkt.info, arrival_time)
                client_db_insert(db, pkt.addr2, pkt.info, arrival_time, day_of_week)
        except AttributeError:
            pass


'''
create a sqlite3 db with unique rows, this ignores duplicate rows which may come in with the same timestamp.
also keeps the db small but allows the same client record inserted with a later time stamp. '''

if __name__ == '__main__':
    try:
        db = sqlite3.connect(sqlite3_db)
        db.text_factory = str
        db.execute('CREATE TABLE IF NOT EXISTS clients(dow text, date text, \
                client text, ssid text, UNIQUE(dow, date, client, ssid))')
        db.commit()
        sniff(iface="wlan1", count=0, prn=pkt_handler, \
                lfilter=lambda p: p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp) \
                or p.haslayer(Dot11ProbeReq), store=0)
        db.close()
    except Exception as e:
        db.close()
        print(e)
    finally:
        db.close()




