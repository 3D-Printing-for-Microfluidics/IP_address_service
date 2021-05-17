import subprocess
from time import sleep

subprocess.run("chmod 600 ../deploy", shell=True)
subprocess.run("ssh-agent sh -c 'ssh-add ../deploy; git fetch'", shell=True)
subprocess.run(
    "ssh-agent sh -c 'ssh-add ../deploy; git reset --hard origin/master'", shell=True
)

sleep(86400)
