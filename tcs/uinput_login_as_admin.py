#!/bin/env python
# -*- coding: utf-8 -*
# vim: set sw=2:

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

if __name__ == "__main__":
  logger.debug("Starting login")
  common.uinput.play(login_seq)
  common.uinput.is_regex_on_screen("Networking:")
  sys.exit(main())
