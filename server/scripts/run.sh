chmod o+r '/home/test/promlems/'$1'/strategies/'$2
ssh -l test localhost 'ulimit -tvvv '$3' ; python3 shell.py'
chmod o-r '/home/test/problems/'$1'/strategies/'$2
