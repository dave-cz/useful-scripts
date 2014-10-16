#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  AutoReconnect.py
#
#  Reconnect WiFi when internet is down
#

from os import system
from urllib2 import urlopen, URLError
from sys import argv
from datetime import datetime
from time import sleep
from argparse import ArgumentParser

def is_internet_on(timeout = 5, url = 'http://www.google.cz'):
    try:
        urlopen(url, timeout = timeout)
        return True
    except URLError: pass # as err
    return False

def reconnect_wifi(name, ssid):
	try:
		system('netsh.exe wlan connect name="{}" ssid="{}"'.format(name, ssid))
	except Exception, ex:
		print ex

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('-s', '--sleeptime', type=int, help="loop period, default = 30 s", default=30)
	parser.add_argument('-t', '--timeout',   type=int, help="server request timeout, default = 5 s", default=5)
	args = parser.parse_args()
	
	print "\nTimeout: {} s\nSleep Time: {} s\n".format(args.timeout, args.sleeptime)
	while True:
		if is_internet_on(args.timeout):
			print "OK:", datetime.now().time()
		else:
			print "Restarting WiFi Connection", datetime.now().time()
			reconnect_wifi('SviZaCha', 'SviZaCha')
			print "\nRestarting WiFi Done", datetime.now().time()
			
		sleep(args.sleeptime)
	
