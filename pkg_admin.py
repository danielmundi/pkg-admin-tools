#!/usr/bin/python3
# pylint: disable=line-too-long

from modules.installer_utils import *

import configparser
import argparse
import requests
import sys


if not os.geteuid() == 0:
    print("\n---------------------------------------------")
    print(" You must be root to run this script")
    print(" (use 'sudo script_installer.py') - exiting")
    print("---------------------------------------------\n")
    exit()

# Read config file
configs = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
configs.read('modules/modules.ini')
config_choices = configs.sections()

# read version file
this_version = read_file(configs['pkg_admin']['install_dir'] + "/version.txt")

# create parser args
parse_descr = "Package install utility for the WLAN Pi. \n"
parser = argparse.ArgumentParser(description=parse_descr)

# check we have passed args of some type
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

# setup parse args
parser.add_argument("-i", dest='install', type=str, metavar=('module'), choices=config_choices, help="install module")
parser.add_argument("-r", dest='roll_back', type=str, metavar=('module'), choices=config_choices, help="rollback module")
parser.add_argument("-d", dest='dev', action='store_true', help="install dev branch (used with -i option)")
parser.add_argument("-b", dest='branch', type=str, metavar=('branch_name'), help="install branch specific branch/release (used with -i option)")
parser.add_argument("-u", dest='update', action='store_true', help="update this utility with latest version")
parser.add_argument("-e", dest='empty_bin', action='store_true', help="empty recycle bin folder")
parser.add_argument("-v", action='version', version=this_version)

args = parser.parse_args()

print()
print("-" * 50)
print("Installer script started...")

branch = "master"
if args.dev:
    branch = "dev"
if args.branch:
    branch = args.branch

# empty recycle bin
if (args.empty_bin):
    if not empty_recycle_bin():
        exit()

# update util
if (args.update):
    instal_module = 'pkg_admin'
else:
    install_module = args.install

if (install_module is not None):
    params = dict(configs.items(install_module))
    post_install = params.get('post_install', '').splitlines()
    del params['post_install']

    pkg_install(branch, params, post_install)

if (args.roll_back is not None):
    params = dict(configs.items(args.roll_back))
    pkg_rollback(params)



# end
print("-" * 50)
exit()
