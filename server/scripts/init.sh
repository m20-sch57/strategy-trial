#!/bin/bash

chmod o-rwx "/home/dba/problems" -R
chmod g-rw "/home/dba/problems" -R
chmod g+x "/home/dba/problems" -R
chmod g+r "/home/dba/problems/$1/classes.py"
