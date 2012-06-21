#!/bin/bash

#
# DESCRIPTION
#

COMMONLIB=${IGOR_LIBDIR}/common/common.sh
[[ -e $COMMONLIB ]] && . $COMMONLIB

FAILED=false

SERVICES="ovirt sshd"

for SERVICE in $SERVICES
do
  if service $SERVICE status;
  then
    echo "Running: $SERVICE"
  else
    echo "NOT running: $SERVICE"
    FAILED=true
  fi
done

if $FAILED;
then
  exit 1
fi

exit 0
