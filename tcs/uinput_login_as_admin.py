#!/bin/env python
# -*- coding: utf-8 -*
# vim: set sw=4:

import sys
import os
import logging
import time

sys.path.append(os.environ["IGOR_LIBDIR"])
import common.input

logger = logging.getLogger(__name__)


story = [
    # Enter Nothing, wait 0 seconds, expect "Please Login" on screen
    (None,                0, "Please login"),

    # Enter …, wait … seconds, expect … on screen
    ("admin\n",           2, "Password:"),

    # Password (taken from set admin password)
    ("ovirt\n",           5, "Networking:")
]


def main():
    logger.debug("Starting simulated TUI login")
    passed = False

    try:
        passed = common.input.suits_storyboard(story)
    except Exception as e:
        logger.warning(e.message)
        passed = False
    logger.debug("Finished simulated TUI login")

    # Check for the TUI lock
    passed = passed and os.path.exists("/tmp/ovirt-setup.tty1")

    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
