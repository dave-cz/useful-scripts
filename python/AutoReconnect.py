#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoReconnect

Reconnect WiFi when internet is down

TODO: start Wi-Fi, if off: Win+X, T
"""
import os
from WindowFinder import WindowFinder
from SendKeys import SendKeys
from urllib2 import urlopen  # , URLError
from datetime import datetime
from time import sleep
from argparse import ArgumentParser


class AutoReconnect(object):
    """ Reconnect WiFi when internet is down """
    def __init__(self, args=None):
        """ Class initialiser """
        self.sleeptime = args['sleeptime']
        self.timeout = args['timeout']
        self.name = args['name']
        self.ssid = args['ssid']
        self.miranda = args['miranda']
        self.url = 'http://www.google.com'
        self.command = 'netsh.exe wlan connect name="{}" ssid="{}"'
        self.logdir = os.path.dirname(os.path.abspath(__file__))
        self.logfile = 'timeout.log'

    def loop(self):
        while True:
            if self.is_internet_on():
                print "OK:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                self.log('Connection timeout at '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.reconnect()
                if self.miranda:
                    sleep(10)
                    try:
                        self.set_miranda_online()
                    except Exception, ex:
                        print ex
            sleep(self.sleeptime)

    def is_internet_on(self):
        try:
            urlopen(self.url, timeout=self.timeout)
            return True
        except Exception:
            pass
        return False

    def reconnect(self):
        try:
            os.system(self.command.format(self.name, self.ssid))
        except Exception, ex:
            print ex

    def log(self, message):
        print 'Log: ', message
        with open(self.logdir+'\\'+self.logfile, 'ab+') as fh_log:
            fh_log.write(message+'\n')

    @staticmethod
    def set_miranda_online():
        """
            Find Miranda window, activate and set online
        """
        win = WindowFinder()
        win.find_window_wildcard('Miranda')
        win.set_foreground()
        SendKeys('^(+)')  # Ctrl + '+'
        SendKeys('{ENTER}')  # Confirm window 'Change online message'

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--sleeptime', type=int, help="loop period, default = 30 s", default=30)
    parser.add_argument('-t', '--timeout', type=int, help="server request timeout, default = 5 s", default=5)
    parser.add_argument('-n', '--name', help="Wifi Network Name, default = 'SviZaCha'", default='SviZaCha')
    parser.add_argument('-ssid', '--ssid', help="Wifi Network SSID, default = 'SviZaCha'", default='SviZaCha')
    parser.add_argument('-m', '--miranda', help="Set Miranda IM online, default = True", default=True)

    args_reconnect = vars(parser.parse_args())
    AutoReconnect(args_reconnect).loop()
