import subprocess
from time import sleep

while True:
    # Pull repository from git using deploy keys
    subprocess.run("chmod 600 ../deploy", shell=True)
    subprocess.run("ssh-agent sh -c 'ssh-add ../deploy; git fetch'", shell=True)
    subprocess.run(
        "ssh-agent sh -c 'ssh-add ../deploy; git reset --hard origin/master'", shell=True
    )

    # Wait 24 hours
    sleep(86400)
