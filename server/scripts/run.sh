chmod o+r '/home/test/problems/'$1'/strategies/'$2
ssh -l test -E ../.strategy-trial.ssh.log localhost 'ulimit -t '$3' ; python3 shell.py || exit $?' || exit $?
chmod o-r '/home/test/problems/'$1'/strategies/'$2
