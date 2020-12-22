from __future__ import print_function
import re
import requests
from orionsdk import SwisClient
import sys

file = sys.argv[1]

def create_node(name_tid, ip_address, oob_ip_address):
    npm_server = 'serverip'
    username = 'username'
    password = 'password'

    swis = SwisClient(npm_server, username, password)
    print("Adding node with ping..")

    # # fill these in for the node you want to add!
    # name_tid = 'xxxxxxx'
    # ip_address = '1.1.1.1'
    # oob_ip_address = '2.2.2.2'
#    community = 'public'

    # set up property bag for the new node
    props = {
        'Caption': name_tid,
        'IPAddress': ip_address,
        'EngineID': 1,
        'ObjectSubType': 'ICMP',
        
    }

    print("Adding node {}... ".format(props['IPAddress']), end="")
    results = swis.create('Orion.Nodes', **props)
    print("DONE!")

    # extract the nodeID from the result
    nodeid = re.search('(\d+)$', results).group(0)

    # add extra custom properites :D
    custom_props = {
        'MY_PROPERTY_1': oob_ip_address,
        'MY_PROPERTY_2': 'client name',
    }
    
    for k,v in custom_props.items():
        swis.update(results + '/CustomProperties', **{k: v})

    pollers_enabled = {
        'N.Status.ICMP.Native': True,
        'N.Status.SNMP.Native': False,
        'N.ResponseTime.ICMP.Native': True,
        # 'N.ResponseTime.SNMP.Native': False,
        # 'N.Details.SNMP.Generic': False,
        # 'N.Uptime.SNMP.Generic': False,
        # 'N.Cpu.SNMP.HrProcessorLoad': False,
        # 'N.Memory.SNMP.NetSnmpReal': False,
        # 'N.AssetInventory.Snmp.Generic': False,
        # 'N.Topology_Layer3.SNMP.ipNetToMedia': False,
        # 'N.Routing.SNMP.Ipv4CidrRoutingTable': False
    }

    pollers = []
    for k in pollers_enabled:
        pollers.append(
            {
                'PollerType': k,
                'NetObject': 'N:' + nodeid,
                'NetObjectType': 'N',
                'NetObjectID': nodeid,
                'Enabled': pollers_enabled[k]
            }
        )

    for poller in pollers:
        print("  Adding poller type: {} with status {}... ".format(poller['PollerType'], poller['Enabled']), end="")
        response = swis.create('Orion.Pollers', **poller)
        print("DONE!")


requests.packages.urllib3.disable_warnings()


def main():
    with open(file, 'r') as f:
        for line in f:
            x = line.strip()
            name_tid, ip_address, oob_ip_addres = x.split()
            try:
                create_node(name_tid, ip_address, oob_ip_addres)
            except Exception as e:
                print(e) 
                
if __name__ == '__main__':
    main()
