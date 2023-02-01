#!/usr/bin/env python3
import logging
import sys
import os
import shutil
import platform
import json
from pathlib import Path

MINIMUM_VERSION = 13.0
CURRENT_VERSION = platform.mac_ver()[0]

def get_user_home_path():
    return os.path.expanduser("~")


def identify_dropbox_location():
    try:
        with open(os.path.expanduser("~/.dropbox/info.json")) as f:
            personal_dropbox_path = Path(json.load(f)["personal"]["path"])
    except Exception:
        print("Couldn't locate Dropbox folder or read info.json. Exiting.")
        sys.exit(1)
    return personal_dropbox_path


def verify_local_rekordbox_library():
    try:
        if (
            os.path.exists(os.path.expanduser("~/Library/Application Support/Pioneer"))
            and os.path.exists(os.path.expanduser("~/Library/Application Support/rekordboxAgent"))
        ):
            print("Identified local Rekordbox Library files")
            return True
        else:
            print("Couldn't locate local Rekordbox Library folders. Aborting.")
            return False
    except Exception:
        print("Couldn't locate Pioneer folder in Application Support. Aborting.")
        sys.exit(1)


def move_folder(src, dst):
    try:
        shutil.move(src, dst)
        print(f"Successfully moved '{src}' to '{dst}'.")
    except Exception as e:
        print(f"Error moving '{src}': {e}")


def link_folder(src, dst):
    try:
        os.symlink(src, dst, target_is_directory=True)
        print(f"Successfully created symbolic link from {src} to {dst}")
    except FileExistsError:
        print(f"Link already exists at {dst}. Skipping.")
    except OSError as e:
        print(f"Failed to create symbolic link from {src} to {dst}. Error: {e}")


def migrate_library(user_home_path, dropbox_library_path):
    pioneer_lib_path = f"{user_home_path}/Library/Pioneer"
    pioneer_app_support_path = f"{user_home_path}/Library/Application Support/Pioneer"
    rekordboxagent_app_support_path = f"{user_home_path}/Library/Application Support/rekordboxAgent"
    
    os.makedirs(f"{dropbox_lib_path}/Application Support", exist_ok=True)
    if (
        not os.path.exists(f"{dropbox_library_path}/Pioneer")
        and not os.path.exists(f"{dropbox_library_path}/Application Support/Pioneer")
        and not os.path.exists(f"{dropbox_library_path}/Application Support/rekordboxAgent")
    ):
        move_folder(pioneer_lib_path, dropbox_library_path)
        move_folder(pioneer_app_support_path, f"{dropbox_library_path}/Application Support")
        move_folder(rekordboxagent_app_support_path, f"{dropbox_library_path}/Application Support")

        link_folder(f"{dropbox_library_path}/Pioneer", f"{user_home_path}/Library/Pioneer")
        link_folder(f"{dropbox_library_path}/Application Support/Pioneer", f"{user_home_path}/Library/Application Support/Pioneer")
        link_folder(f"{dropbox_library_path}/Application Support/rekordboxAgent", f"{user_home_path}/Library/Application Support/rekordboxAgent")
        
        print("Successfully migrated Pioneer Rekordbox Library to Dropbox cloud.")
    else:
        print(f"Found existing Rekordbox Library files in '{dropbox_library_path}'. Aborting.")
        sys.exit(1)
    

if __name__ == "__main__":
    if float(CURRENT_VERSION) >= MINIMUM_VERSION:
        print(f"Running supported macOS version {CURRENT_VERSION}. Continuing.")
        user_home_path = get_user_home_path()
        dropbox_path = identify_dropbox_location()
        if dropbox_path:
            use_dropbox = input(f"Identified Dropbox path: '{dropbox_path}'. Use this path? [yes/no]: ").lower() == "yes"
            if use_dropbox:
                dropbox_rb_folder = input("Specify the Dropbox folder for the library [Default 'RekordboxLibrary']: ") or "RekordboxLibrary"
                dropbox_lib_path = f"{dropbox_path}/{dropbox_rb_folder}"
                if input(f"Storing library under '{dropbox_lib_path}'. Continue? [yes/no]: ").lower() == "yes":
                    if not os.path.exists(f"{dropbox_lib_path}"):
                        print(f"Creating folder {dropbox_lib_path}")
                        os.makedirs(f"{dropbox_lib_path}")
                    else:
                        print("Folder already exists. Continuing.")
                    migrate = input("Migrate local library to Dropbox now? [yes/no]: ") == "yes"
                    if migrate:
                        if verify_local_rekordbox_library():
                            migrate_library(user_home_path, dropbox_lib_path)
        else:
            print("Dropbox path is empty. Aborting.")
            sys.exit(1)
    else:
        print(f"Running unsupported macOS version {CURRENT_VERSION}. Aborting.")
        sys.exit(1)
