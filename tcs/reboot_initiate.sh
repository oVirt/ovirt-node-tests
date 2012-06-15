#!/bin/bash

. /usr/libexec/ovirt-functions

step_succeeded
reboot

# Don't continue, we want to restart
sleep 60

exit 0
