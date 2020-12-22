#! /usr/bin/python
## 
##  Karsten Iwen
##  please send bug-reports, comments or improvements to:
##  ki@security-planet.de
##
##  Version 1.0

import sys

if len(sys.argv) == 3:

	file_arp = open(sys.argv[1], 'r')
	file_dhcp = open(sys.argv[2], 'r')

	arr_arp = []
	arr_arp2 = []
	arr_dhcp = []

	for line in file_arp.readlines():
		values = line.split()
		arr_arp.append(values)
		arr_arp2.append(values)
	for line in file_dhcp.readlines():
		values = line.split()
		arr_dhcp.append(values)

	for i1 in range(len(arr_arp)):
		for i2 in range(len(arr_dhcp)):
			if arr_arp[i1][1] == arr_dhcp[i2][1]:
				arr_arp2.remove(arr_arp[i1])

	for i in range(len(arr_arp2)):
		print arr_arp2[i]

else:
	print ("dai-check.py compares the ARP-Table of a Cisco L3-Switch (show arp | i VlanXX)")
	print ("with the DHCP-Snooping-Database of a Cisco-Switch (show ip dhcp snooping binding vlan XX | i dhcp-snooping)")
	print ("")
	print ("Version 1.0")
	print ("")
	print ("Usage:")
	print ("======")	
	print ("dai-check.py <File with ARP-Table> <File with DHCP-Snooping-Table>")
	print ("")
	print ("Written by:")
	print ("===========")
	print ("Karsten Iwen")
	print ("ki@security-planet.de")
	print ("http://security-planet.de")
	print ("")
