"""
lima 6/16/2017
multiprocessing works better in linux... forking is not supported in windows
... just run this in linux and move on...
12
"""
#!/usr/bin/env python
# from __future__ import absolute_import, division, print_function
import netmiko
# import my toolbox.py functions
import toolbox
from multiprocessing import pool
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOerror on broken pipe

signal.signal(signal.SIGINT, signal.SIG_DFL) # hanlde keyboard interrupt and exit

device_type = 'cisco_asa'

username, password = toolbox.get_credentials()

device_ip = '''
10.x.y.z
10.x.y.z
'''.strip().splitlines()


def my_function(i):
    try:
        connection = netmiko.ConnectHandler(ip=i, device_type='cisco_asa', username=username, password=password,
                                            secret=password)

        hostname = connection.find_prompt()
        connection.config_mode()
        x = connection.send_command('sh run ssh | i 10.x.y.z')
        x = connection.send_command('no logging host Inside 1.2.2.2')
        connection.disconnect()
        print '%s: %s' % (hostname, 'done')

    except Exception as e:
        print '%s: %s' % (i, e)


pool = Pool(16)
pool.map(my_function, device_ip)
