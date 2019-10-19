#!/bin/bash

chmod g+r "/home/dba/problems/$1/strategies/$2"
su -- test -c "ulimit -t $3; ulimit -v 262144; unshare -rn python3 shell.py"
retcode=$?
chmod g-r "/home/dba/problems/$1/strategies/$2"
exit $retcode
