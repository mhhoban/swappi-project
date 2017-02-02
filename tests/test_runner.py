import subprocess
import sys

if sys.argv[1] == '-unit':
    subprocess.call('python tests/unit/unit_test_runner.py', shell=True)

elif sys.argv[1] == '-functional':
    print('functional tests not yet implemented')

else:
    print('invalid selection, provide either -unit or -functional as argument')
