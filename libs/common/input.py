#!/bin/env python
# -*- coding: utf-8 -*
# vim: set sw=4:

import sys
import os
import logging
import time
import re
import random
import time

import common

#
# Import python-uinput
#
common.run("modprobe uinput")
UINPUTPYDIR = os.path.join(common.igor.libdir, \
                         "uinput/dst/lib64/python2.7/site-packages/")
sys.path.append(UINPUTPYDIR)
import uinput


logger = logging.getLogger(__name__)
logger.debug("UINPUTPYDIR: %s" % UINPUTPYDIR)


class PressedKey(object):
    key = None

    def __init__(self, k):
        self.key = k

    def __enter__(self):
        device.emit(self.key, 1)

    def __exit__(self, type, value, traceback):
        device.emit(self.key, 0)


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
        ".": "dot",
        "-": "minus",
        "+": "plus",
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
    with PressedKey(key):
        time.sleep(1.0 / 100 * delay * random.uniform(0.5, 1.5))


def send_input(txt):
    """Send the string as keystrokes to uinput
    """
    logger.debug("Inputing: %s" % txt)
    for char in txt:
        if char.isupper():
            with PressedKey(uinput.KEY_LEFTSHIFT):
                press_key(char_to_key(char.lower()))
        else:
            press_key(char_to_key(char.lower()))


def play(seq):
    """Plays a sequence of text, single keys and callables
    """
    for item in seq:
        if callable(item):
            item()
        elif type(item) is tuple:
            # Expected to be a uinput.KEY_
            press_key(item)
        elif type(item) in [str, unicode]:
            send_input(item)
        else:
            logger.warning("Unknown sequence type: %s (%s)" % (type(item), \
                                                               item))


def screen_content(vcsn=1):
    vcs = "/dev/vcs%s" % vcsn
    logger.debug("Grabbing content from '%s'" % vcs)
    # setterm -dump $N
    content = open(vcs, "r").read()
    return content


def is_regex_on_screen(expr, vcsn=1):
    """Check if the given expression appears on the screen.
    """
    content = screen_content(vcsn)
    logger.debug("Looking for '%s' on '%s'" % (expr, vcsn))
    regex = re.compile(expr)
    return regex.search(content) is not None


def suits_storyboard(story):
    """Checks a "storyboard"
    A storyboard is expected to be in the form of:
    story = [
        (input_for_play, output_for_is_regex_on_screen_or_callable),
        .
        .
        .
    ]
    """
    passed = True
    for storyline in story:
        logger.info("Testing: %s" % str(storyline))

        input, wait, output = storyline
        if input is None:
            logger.debug("No input to send")
        else:
            play(input)

        time.sleep(wait)

        if output is None:
            logger.debug("No output expected")
        elif callable(output):
            passed = output(input)
        else:
            passed = is_regex_on_screen(output)

        if passed == False:
            content = screen_content()
            raise Exception("Response is not as expected.\n" + \
                            "Sent: %s\nExpected: %s\nGot: %s" % (input, \
                                                                 output, \
                                                                 content))
    return passed

device = uinput.Device(_all_keys())
