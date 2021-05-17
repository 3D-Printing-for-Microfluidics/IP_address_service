import subprocess
import os

RELEASE = "master"  # default release
REPO_NAME = "IP_address_service"
UPDATE_CMD = (  # base command
    'pip3 install --src="%s" --upgrade -e '
    "git+https://github.com/3D-Printing-for-Microfluidics/IP_address_service.git@%s#egg=%s"
)

os.chdir("../..")
src_dir = os.getcwd()
release = RELEASE
commit = None

release = "origin/" + release
cmd = UPDATE_CMD % (src_dir, release, REPO_NAME)
try:
    subprocess.run(cmd, shell=True)
except OSError:
    print(cmd)
    print("Update failed")
    pass

# os.chdir("ip-address-service")
# subprocess.run("rm setup.py", shell=True)
# subprocess.run("rm -r UNKNOWN.egg-info", shell=True)
# subprocess.run("pip3 uninstall -y unknown", shell=True)
