#!/bin/bash

chgrp test problems -R
chmod o-rwx "/home/dba/problems" -R
chmod g-rw "/home/dba/problems" -R
chmod g+rx "/home/dba/problems"
chmod g+rx "/home/dba/problems/$1"
chmod g+rx "/home/dba/problems/$1/strategies"
chmod g+r "/home/dba/problems/$1/classes.py"
