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

class AutoReconnect:
	def __init__ (self, args):
		""" Class initialiser """
		self.__dict__.update(args.__dict__)
		self.url = 'http://www.google.com'
		self.command = 'netsh.exe wlan connect name="{}" ssid="{}"'.format(self.name, self.ssid)
	
	def loop(self):
		while True:
			if self.is_internet_on():
				print "OK:", datetime.now().time()
			else:
				print "Restarting WiFi Connection", datetime.now().time()
				self.reconnect()
				print "\nRestarting WiFi Done", datetime.now().time()
			
			sleep(self.sleeptime)

	def is_internet_on(self):
		try:
			urlopen(self.url, timeout = self.timeout)
			return True
		except URLError: pass
		return False

	def reconnect(self):
		try:
			system(self.command)
		except Exception, ex:
			print ex

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('-s', '--sleeptime', type=int, help="loop period, default = 30 s", default=30)
	parser.add_argument('-t', '--timeout', type=int, help="server request timeout, default = 5 s", default=5)
	parser.add_argument('-n', '--name', help="Wifi Network Name, default = 'SviZaCha'", default='SviZaCha')
	parser.add_argument('-ssid', '--ssid', help="Wifi Network SSID, default = 'SviZaCha'", default='SviZaCha')
	args = parser.parse_args()
	
	AutoReconnect(args).loop()
