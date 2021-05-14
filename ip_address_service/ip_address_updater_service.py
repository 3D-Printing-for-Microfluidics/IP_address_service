from subprocess import call as run
import os

RELEASE = "master"  # default release
# SRC_DIR = "$HOME/.printer_ip_service"  # checkout directory
REPO_NAME = "IP_address_service"
UPDATE_CMD = (  # base command
    'pip3 install --src="%s" --upgrade -e '
    "git+https://github.com/3D-Printing-for-Microfluidics/IP_address_service.git@%s#egg=%s --verbose"
)

# @command
# def update(args):
#     try:
#         opts, args = getopt(args, 'sr:', ['sudo', 'src=', 'release=', 'commit='])
#     except GetoptError, err:
#         log(err)
#         usage(error_codes['option'])

#     sudo = False
#     src_dir = SRC_DIR
#     release = RELEASE
#     commit = None
# for opt, arg in opts:
#     if opt in ('-s', '--sudo'):
#         sudo = True
#     elif opt in ('-r', '--release'):
#         release = arg
#     elif opt in ('--src',):
#         src_dir = arg
#     elif opt in ('--commit',):
#         commit = arg

# if release[0].isdigit(): ## Check if it is a version
#     release = 'r' + release
# release = 'origin/' + release ## assume it is a branch

# if commit is not None: ## if a commit is supplied use that
#     cmd = UPDATE_CMD % (src_dir, commit)
# else:
#     cmd = UPDATE_CMD % (src_dir, release)

# if sudo:
#     run('sudo %s' % cmd)
# else:
#     run(cmd)

sudo = False
# src_dir = SRC_DIR
os.chdir("../..")
src_dir = os.getcwd()
release = RELEASE
commit = None

release = "origin/" + release
cmd = UPDATE_CMD % (src_dir, release, REPO_NAME)
try:
    run(cmd)
except OSError:
    print(cmd)
    print("Update failed")
    pass
