import os
import re

with open('arp.txt', 'r') as f:

a = re.search(
    r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*((([0-9a-f]{2}\:?){6})|(([0-9a-f]{4}\.?){3})).*', line)


def my_func(mac_list):
    for line in mac_list:
        my_filter = re.search(
            r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*((([0-9a-f]{2}\:?){6})|(([0-9a-f]{4}\.?){3})).*', line)
        if my_filter:
            _x = my_filter.group(1)
            _z = re.sub('[:.]', '', my_filter.group(2))
            _y = ':'.join(_z[i:i + 2] for i in range(0, 12, 2))
            if not _x or not _y:
                continue
            else:
                print "IP: " + _x + " MAC: " + _y

