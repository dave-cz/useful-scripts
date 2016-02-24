#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WindowFinder

Source: http://stackoverflow.com/a/17350440
"""

import win32gui
import re  # , SendKeys


class WindowFinder(object):
    """ Class to find and make focus on a particular Native OS dialog/Window """

    def __init__(self):
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """ Pass a window class name & window name directly if known to get the window """
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """ Call back func which checks each open window and matches the name of window using reg ex """
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """ This function takes a string as input and calls EnumWindows to enumerate through all open windows """
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """ Get the focus on the desired open window """
        win32gui.SetForegroundWindow(self._handle)


if __name__ == '__main__':
    pass
    # win = WindowFinder()
    # win.find_window_wildcard(".*Save As.*")
    # win.set_foreground()
    # path = "D:\\File.txt"            # Path of the file you want to Save
    # ent = "{ENTER}"                  # Enter key stroke.
    # SendKeys.SendKeys(path)          # Use SendKeys to send path string to Save As dialog
    # SendKeys.SendKeys(ent)           # Use SendKeys to send ENTER key stroke to Save As dialog
