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
    # P. 1 Welcome
    # Press nothing, wait 0 seconds, expect "Install …"
    (None,                0, "Install Hypervisor"),

    # P. 2: Enter keyboard selection
    # Press ENTER, wait 4 seconds, expect "Keyboard …"
    ("\n",                4, "Keyboard Layout Selection"),

    # P. 2: Select german keyboard layout
    # Press 53 times UP, wait 0 seconds and expect "German"
    (53 * [common.input.uinput.KEY_UP], 0, "German"),

    # P. 3: Enter boot device selection
    # Press ENTER wait 4 seconds and expect "booting …"
    ("\n",                4, "booting oVirt Node"),

    # P. 4: Enter installation device selection
    ("\n",                4, "installation of oVirt Node"),

    # P. 5: Enter password dialog
    ("\t\t\t\n",          4, "Require a password"),
    ("ovirt\tovirt\t",    1, "a weak password"),

    # P. 6: Start installation
    ("\t\t\n",          120, "Installation Finished"),

    # P. 7: Reboot
    ("\n", 0, None)
]

def main():
    logger.debug("Starting simulated TUI installation")
    passed = False

    try:
        passed = suits_storyboard(story):
    except Exception e:
        logger.warning(e.message)
    logger.debug("Finished simulated TUI installation")

    return 1 if passed else 0

if __name__ == "__main__":
    sys.exit(main())
