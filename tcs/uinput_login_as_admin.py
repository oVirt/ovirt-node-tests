#!/bin/env python
# -*- coding: utf-8 -*
# vim: set sw=4:

import sys
import os
import logging
import time

sys.path.append(os.environ["IGOR_LIBDIR"])
import common.uinput


logger = logging.getLogger(__name__)


login_seq = [
    # User
    "admin\n",
    lambda: time.sleep(0.7),
    # Password (taken from set admin password)
    "ovirt\n",
    lambda: time.sleep(4),
]


def main():
    logger.debug("Starting login")
    common.uinput.play(login_seq)
    on_screen = common.uinput.is_regex_on_screen("Networking:")
    lock_exists = os.path.exists("/tmp/ovirt-setup.tty1")

    if on_screen and lock_exists:
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
