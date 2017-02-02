import subprocess

subprocess.call('python -m unittest discover -s . -p *_tests.py',
                shell=True)
