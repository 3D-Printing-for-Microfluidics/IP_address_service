import subprocess
import os

subprocess.run("chmod 600 ../deploy", shell=True)
subprocess.run("ssh-agent sh -c 'ssh-add ../deploy; git fetch'", shell=True)
subprocess.run("ssh-agent sh -c 'ssh-add ../deploy; git pull'", shell=True)
