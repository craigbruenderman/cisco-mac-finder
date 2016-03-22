#!/usr/bin/env python

import paramiko
import time
import re

def list_macs(client):
    stdin, stdout, stderr = client.exec_command('sh mac addr dyn \n')
    entries = []
    for line in stdout:
        #line = line.strip('\n')
        vlan = re.findall('(\d{1,4})\s', line)
        mac = re.findall('\w{4}.\w{4}.\w{4}', line)
        interface = re.findall('Gi[\d]/[\d]/[\d]|Po[\d]+', line)
        
        if vlan != None and len(vlan) > 0 and mac != None and len(mac) > 0:
            entries.append([mac[0], vlan[0], interface[0]])
            
    for entry in entries:
        print 'Found MAC %s in VLAN %s on interface %s' % (entry[0], entry[1], entry[2])
        

def find_mac(client, mac):
    stdin, stdout, stderr = client.exec_command('sh mac addr add ' + mac + '\n')
    for line in stdout:
        print line.strip('\n')
        goodput = re.findall('[a-f0-9]{4}.[a-f0-9]{4}.[a-f0-9]{4}', line)
        if goodput != None and len(goodput) > 0:
            print goodput


if __name__ == '__main__':

    ip = '192.168.10.7'
    username = 'craigb'
    password = raw_input('Gimme the goods: ')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "connected to %s" % ip
    
    list_macs(client)
    #find_mac(client, 'dc9f.db5e.e5b1')
