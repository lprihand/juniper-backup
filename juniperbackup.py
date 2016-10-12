#!/usr/bin/env python
#
#
#

import paramiko
import time
import os

def disable_paging(remote_conn):
	'''Disable paging on a Juniper router'''
	time.sleep(1)
	output = remote_conn.recv(1000)
	return output

if __name__ == '__main__':
	ipaddress = open("list.txt","r")
	username = 'lukman'
	password = 'superman'
for i in ipaddress.readlines():
	ip = i.split()
# Create instance of SSHClient object
	remote_conn_pre = paramiko.SSHClient()
# Automatically add untrusted hosts (make sure okay for security policy in your environment)
	remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# initiate SSH connection
	remote_conn_pre.connect(ip[0], username=username, password=password)
	print '#################################################'
	print "SSH connection established to %s" % ip[0]
# Use invoke_shell to establish an 'interactive session'
	remote_conn = remote_conn_pre.invoke_shell()
# print "Interactive SSH session established"
# Strip initial prompt
	output = remote_conn.recv(1000)
# Send the router a command
	remote_conn.send("set cli screen-length 10000\n")
	time.sleep(1)
	remote_conn.send("show configuration | display set\n")
	time.sleep(2)
	remote_conn.send("show configuration \n")
# Wait for the command to complete
	time.sleep(2)
	output = remote_conn.recv(500000000)
# print output
# print output
##################
#OUTPUT GENERATED FOR FILES
###########################
	mytime = time.strftime('@%Y-%m-%d@%H-%M-%S')
	ip = ip[0].strip(' \t\n\r')
	print
	print ip + ' config backup in place'
	print
	filename = ("Backup@" + ip + mytime + ".cfg")
	filepath = os.path.join('configs', ip, filename)
	if not os.path.exists(os.path.dirname(filepath)):
		os.makedirs(os.path.dirname(filepath))
	with open(filepath, "w") as f:
		f.write(output)
		f.close()
#disconnect
	remote_conn.send("exit\n")
	print "SSH connection closed to %s" % ip
	print '#################################################'
