#!/bin/bash

chmod o+r '/home/test/problems/'$1'/strategies/'$2
su - test -c "ulimit -t $3 ; python3 shell.py"
retcode=$?
chmod o-r '/home/test/problems/'$1'/strategies/'$2
exit $retcode
