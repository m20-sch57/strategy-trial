chmod o+r '/home/test/problems/'$1'/strategies/'$2
ssh -l test localhost 'ulimit -t '$3' ; python3 shell.py || exit $?' || exit $?
chmod o-r '/home/test/problems/'$1'/strategies/'$2
