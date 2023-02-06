#!/usr/bin/env python3
# INSTALL /usr/bin/env python3 -c "$(curl -fsSL https://raw.githubusercontent.com/nicolaswehmeyer/rekordbox-dropbox-library-sync/main/main.py)"
import logging
import sys
import os
import shutil
import platform
import json
from pathlib import Path

MINIMUM_VERSION = 13.0
CURRENT_VERSION = platform.mac_ver()[0]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_user_home_path():
    return os.path.expanduser("~")


def identify_dropbox_location():
    try:
        with open(os.path.expanduser("~/.dropbox/info.json")) as f:
            personal_dropbox_path = Path(json.load(f)["personal"]["path"])
    except Exception:
        print(f"{bcolors.FAIL}Couldn't locate Dropbox folder or read info.json. Exiting.{bcolors.ENDC}")
        sys.exit(1)
    return personal_dropbox_path


def verify_local_rekordbox_library():
    try:
        if os.path.exists(os.path.expanduser("~/Library/Pioneer")):
            print(f"{bcolors.OKGREEN}Identified local Rekordbox Library files.{bcolors.ENDC}")
            return True
        else:
            print(f"{bcolors.FAIL}Couldn't locate local Rekordbox Library folders. Aborting.{bcolors.ENDC}")
            return False
    except Exception:
        print(f"{bcolors.FAIL}Couldn't locate local Pioneer folder in users 'Library' folder. Aborting.{bcolors.ENDC}")
        sys.exit(1)


def move_folder(src, dst):
    try:
        shutil.move(src, dst)
        print(f"{bcolors.OKGREEN}Successfully moved '{src}' to '{dst}'.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}Error moving '{src}': {e}.{bcolors.ENDC}")


def link_folder(src, dst):
    try:
        os.symlink(src, dst, target_is_directory=True)
        print(f"{bcolors.OKGREEN}Successfully created symbolic link from {src} to {dst}.{bcolors.ENDC}")
    except FileExistsError:
        print(f"{bcolors.WARNING}Link already exists at {dst}. Skipping.{bcolors.ENDC}")
    except OSError as e:
        print(f"{bcolors.FAIL}Failed to create symbolic link from {src} to {dst}. Error: {e}.{bcolors.ENDC}")


def migrate_library(user_home_path, dropbox_library_path):
    pioneer_lib_path = f"{user_home_path}/Library/Pioneer"
    # pioneer_app_support_path = f"{user_home_path}/Library/Application Support/Pioneer"
    # rekordboxagent_app_support_path = f"{user_home_path}/Library/Application Support/rekordboxAgent"
    # os.makedirs(f"{dropbox_lib_path}/Application Support", exist_ok=True)
    if (
        not os.path.exists(f"{dropbox_library_path}/Pioneer")
        # and not os.path.exists(f"{dropbox_library_path}/Application Support/Pioneer")
        # and not os.path.exists(f"{dropbox_library_path}/Application Support/rekordboxAgent")
    ):
        move_folder(pioneer_lib_path, dropbox_library_path)
        # move_folder(pioneer_app_support_path, f"{dropbox_library_path}/Application Support")
        # move_folder(rekordboxagent_app_support_path, f"{dropbox_library_path}/Application Support")
        link_folder(f"{dropbox_library_path}/Pioneer", f"{user_home_path}/Library/Pioneer")
        # link_folder(f"{dropbox_library_path}/Application Support/Pioneer", f"{user_home_path}/Library/Application Support/Pioneer")
        # link_folder(f"{dropbox_library_path}/Application Support/rekordboxAgent", f"{user_home_path}/Library/Application Support/rekordboxAgent")
        print(f"{bcolors.OKGREEN}Successfully migrated Pioneer Rekordbox Library to Dropbox cloud.{bcolors.ENDC}")
    else:
        if input(f"{bcolors.OKBLUE}Found existing Rekordbox Library files in '{dropbox_library_path}'. Overwrite local database? [yes/no]: {bcolors.ENDC}").lower() == "yes":
            os.rename(pioneer_lib_path, f"{pioneer_lib_path}_backup")
            # os.rename(pioneer_app_support_path, f"{pioneer_app_support_path}_backup")
            # os.rename(rekordboxagent_app_support_path, f"{rekordboxagent_app_support_path}_backup")
            link_folder(f"{dropbox_library_path}/Pioneer", f"{user_home_path}/Library/Pioneer")
            # link_folder(f"{dropbox_library_path}/Application Support/Pioneer", f"{user_home_path}/Library/Application Support/Pioneer")
            # link_folder(f"{dropbox_library_path}/Application Support/rekordboxAgent", f"{user_home_path}/Library/Application Support/rekordboxAgent")
            print(f"{bcolors.OKGREEN}Successfully migrated Pioneer Rekordbox Library to Dropbox cloud.{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Aborted.{bcolors.ENDC}")
            sys.exit(0)
    

def deactivate_rekordbox_agent():
    if input(f"{bcolors.WARNING}This will prevent the Rekordbox Agent from system startup. Continue? [yes/no]: {bcolors.ENDC}").lower() == "yes":
        os.system(": > ~/Library/LaunchAgents/com.pioneerdj.rekordboxdj.agent.plist && \
            chflags uchg ~/Library/LaunchAgents/com.pioneerdj.rekordboxdj.agent.plist")
    else:
        print(f"{bcolors.FAIL}Aborted.{bcolors.ENDC}")
        sys.exit(0)


if __name__ == "__main__":
    os.system('clear')
    if float(CURRENT_VERSION) >= MINIMUM_VERSION:
        print(f"{bcolors.OKGREEN}Running supported macOS version {CURRENT_VERSION}. Continuing...{bcolors.ENDC}")
        user_home_path = get_user_home_path()
        dropbox_path = identify_dropbox_location()
        if dropbox_path:
            use_dropbox = input(f"{bcolors.OKBLUE}Identified Dropbox path: '{dropbox_path}'. Use this path? [yes/no]: {bcolors.ENDC}").lower() == "yes"
            if use_dropbox:
                print(f"{bcolors.OKGREEN}Using '{dropbox_path}'. Continuing...")
                dropbox_rb_folder = input(f"{bcolors.OKBLUE}Please specify the desired Dropbox library folder [Default 'RekordboxLibrary']: {bcolors.ENDC}") or "RekordboxLibrary"
                dropbox_lib_path = f"{dropbox_path}/{dropbox_rb_folder}"
                if input(f"{bcolors.OKBLUE}Storing library under '{dropbox_lib_path}'. Continue? [yes/no]: {bcolors.ENDC}").lower() == "yes":
                    if not os.path.exists(f"{dropbox_lib_path}"):
                        os.makedirs(f"{dropbox_lib_path}")
                        print(f"{bcolors.OKGREEN}Created new folder '{dropbox_lib_path}'.{bcolors.ENDC}")
                    else:
                        print(f"{bcolors.OKGREEN}Folder already exists. Continuing...{bcolors.ENDC}")
                    migrate = input(f"{bcolors.OKBLUE}Migrate local library to Dropbox now? [yes/no]: {bcolors.ENDC}") == "yes"
                    if migrate:
                        if verify_local_rekordbox_library():
                            migrate_library(user_home_path, dropbox_lib_path)
        else:
            print(f"{bcolors.FAIL}Couldn't identify a Dropbox path. Aborting.{bcolors.ENDC}")
            sys.exit(1)
    else:
        print(f"{bcolors.FAIL}Running unsupported macOS version {CURRENT_VERSION}. Aborting.{bcolors.ENDC}")
        sys.exit(1)
