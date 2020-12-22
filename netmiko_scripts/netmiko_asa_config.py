#!/usr/bin/env python

# lima 6/16/2017
# multiprocessing works better in linux... forking is not supported in windows
# ... just run this in linux and move on...
#
# from __future__ import absolute_import, division, print_function
# requires my toolbox.py file

# from netmiko import ConnectionHandler
import netmiko
# import my toolbox.py functions
import toolbox
from multiprocessing import Pool
import json
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOerror on broken pipe

signal.signal(signal.SIGINT, signal.SIG_DFL) # hanlde keyboard interrupt and exit

device_type = 'cisco_asa'

username, password = toolbox.get_credentials()

device_ip = toolbox.get_ips('ip.list.txt')

"""
# different way to feed ips to my_function

device_ip = '''
10.1.1.1
10.1.2.2
'''.strip().splitlines()

"""


def my_function(i):
    try:
        connection = netmiko.ConnectHandler(ip=i, device_type=device_type, username=username, password=password,
                                            secret=password)

        hostname = connection.find_prompt()
        connection.config_mode()
        y = connection.send_command('sh run ssh | i 10\.3\.')

        connection.disconnect()
        print '%s: %s \n' % (hostname, 'done')
        print '%s' % (y)
    except Exception as e:
        print '%s: %s' % (i, e)


pool = Pool(16)
pool.map(my_function, device_ip)

