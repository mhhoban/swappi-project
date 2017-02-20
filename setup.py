import subprocess

print('Starting Setup:')
subprocess.call('mkdir db', shell=True)
subprocess.call('pip install -r requirements.txt', shell=True)

import swappi.db_setup

_db_setup = swappi.db_setup.DbSetup()
_db_setup.db_init()
