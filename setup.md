This is setup guide. For duing some of this things you will need root privileges. So **think *before* type**. Author isn't responsible for any effects.

First, you need to make two users: test and dba
user test should have no home dir, user dba should.
This can be made by useradd comand. Example:
```
    useradd -M test
    useradd -m dba
```
Then you need to enable user dba to substitute user test (via su).
For this you can either delete password for user test (very insecure) or changing the file /etc/pam.d/su:
you need to add this two lines right below the `pam_rootok.so`
```
    auth  [success=ignore default=1] pam_succeed_if.so user = test
    auth  sufficient                 pam_succeed_if.so use_uid user = dba
```
Then you need to go to releases page and download archieve (tar or zip) and unpack it to home dir of dba.
It's important to avoid the 'container directory'.
You can unpack tar archieve using tar command. Example:
```
    tar -xvf <release_version.tar> --strip 1
```
Then you need to set the permitions:
    Owner: dba
    `/home/dba/*` except `shell.py`: group dba, `shell.py`: group test.
    This can be made by chgrp comand.
    Also you need to disable writing and reading to group and others (except `shell.py`). For example:
    ```
        chmod o-rwx /home/dba -R
        chmod g-rw /home/dba -R
        chmod g+r /home/dba/shell.py
    ```
