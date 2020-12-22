#!/usr/bin/env python

# lima 6/16/2017
# multiprocessing works better in linux... forking is not supported in windows
# ... just run this in linux and move on...
#
# from __future__ import absolute_import, division, print_function

import netmiko
from multiprocessing import Pool
# import my toolbox.py functions
import toolbox
# from netmiko import ConnectHandler
import re
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOerror on broken pipe

signal.signal(signal.SIGINT, signal.SIG_DFL) # hanlde keyboard interrupt and exit


device_type = 'cisco_ios'

username, password = toolbox.get_credentials()

device_ip = toolbox.get_ips('ip.list.txt')


def route_lookup(y):
    ''' split string and return last element '''
    return y.split()[-1]


def my_function(i):
    try:
        connection = netmiko.ConnectHandler(
            ip=i, device_type=device_type, username=username, password=password)
        hostname = connection.find_prompt()
        # connection.config_mode()
        # connection.send_command('ssh 10.x.y.0 255.255.255.0 ' + route_lookup(x))
        #        connection.send_command('clock timezone CST -6')
        #        connection.send_command('clock summer-time CST recurring')
        y = connection.send_command(
            'sh run | s ip access-list standard ACL_SSH_VTY_ACCESS')
        # for t in y:
        #   if t:
        #   connection.send(xyz)
        # y = connection.send_command('sh run ssh')

        connection.disconnect()
        print '%s: %s \n' % (hostname, i)
        print '%s' % (y)
    except Exception as e:
        print '%s: %s' % (i, e)

# define number of threads to fire up at once
pool = Pool(16)
pool.map(my_function, device_ip)
