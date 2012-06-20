#!/bin/env python
# -*- coding: utf-8 -*
# vim: set sw=4:

import sys
import os
import logging
import time
import re
import random

import common.common as common

#
# Import python-uinput
#
UINPUTPYDIR = os.path.join(common.igor.libdir, \
                         "uinput/dst/lib64/python2.7/site-packages/")
sys.path.append(UINPUTPYDIR)
import uinput


logger = logging.getLogger(__name__)


def _all_keys():
    """Fetches all key related capabilities.
    """
    keys = []
    for k in uinput.__dict__:
        if re.match("^KEY_", k):
            keys.append(uinput.__dict__[k])
    return keys


def char_to_key(char):
    """Maps a character to a key-code
    """
    kmap = {
        " ": "space",
        "\t": "tab",
        "\n": "enter"
    }
    if char in kmap:
        char = kmap[char]
    key_key = "KEY_%s" % char.upper()
    return uinput.__dict__[key_key]


def press_key(key, delay=12):
    """Simulates a key stroke
    """
    device.emit(key, 1)
    time.sleep(1.0 / 100 * delay * random.uniform(0.5, 1.5))
    device.emit(key, 0)


def send_input(txt):
    """Send the string as keystrokes to uinput
    """
    logger.debug("Inputing: %s" % txt)
    for char in txt:
        if char.isupper():
            device.emit(uinput.KEY_LEFTSHIFT, 1)
        press_key(char_to_key(char.tolower()))
        if char.isupper():
            device.emit(uinput.KEY_LEFTSHIFT, 0)


def play(seq):
    """Plays a sequence of keystrokes and callables
    """
    for item in seq:
        if callable(item):
            item()
        elif type(item) is str:
            send_input(item)
        else:
            logger.warning("Unknown sequence type: %s (%s)" % (type(item), \
                                                               item))


def is_regex_on_screen(expr, vcsn=1):
    """Check if the given expression appears on the screen.
    """
    vcs = "/dev/vcs%s" % vcsn
    logger.debug("Looking for '%s' on '%s'" % (expr, vcs))
    regex = re.compile(expr)
    # setterm -dump $N
    content = open(vcs, "r").read()
    return regex.search(content) is not None

device = uinput.Device(_all_keys())
