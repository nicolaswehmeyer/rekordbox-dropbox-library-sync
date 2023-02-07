
# Rekordbox Dropbox Library Sync (RDLS)
Sync your Rekordbox library across multiple devices.

## Screenshot
![App Screenshot](https://raw.githubusercontent.com/nicolaswehmeyer/rekordbox-dropbox-library-sync/main/rdls-execution.png)

## Description
**PLEASE USE WITH CAUTION, THIS IS IN VERY EARLY STAGES. I AM NOT RESPONSIBLE FOR ANY DAMAGE YOU MAY EXPERIENCE USING THIS SCRIPT! ALWAYS CREATE A BACKUP OF YOUR CURRENT LIBRARY FIRST!**

Rekordbox Dropbox Library Sync (RDLS) allows you to sync your Rekordbox DJ Library across multiple devices using the Dropbox cloud.

It is a great solution for DJs that already keep their music within their Dropbox and need a way to also sync their local Rekordbox database across several of their devices.

Please note: RDLS will not sync any of your music files (.mp3, .wav, .aiff, etc.) across your devices - it only syncs the actual database files and playlists you created across multiple devices.

## Supported Platforms
RDLS supports Apple's macOS Ventura operating system beginning from version 13.0. Windows, Linux or other Unix operating systems arent't supported.

## How do I run RDLS
RDLS can be executed with a simple one liner and doesn't require administrative prviliges.

**Before installation:**
- Please ensure to stop Rekordbox before running the below command
- It is crucial that Rekordbox is running in version 6.6.9 or above
- Ensure that you've completed the initial setup of Rekordbox by logging in with your user account and creating an initial database. This step is crucial for a successful migration in case of a new Rekordbox installation
- If you already had a local Rekordbox DJ library on your computer, but also synced your Rekordbox DJ library from another computer to the Dropbox folder you specified during the setup of RDLS, RDLS will detect such scenarios and ask for your permission to overwrite your local library with the library stored in your Dropbox folder. All pre-existing Rekordbox DJ Library files will be moved to a *_backup folder

Open a new Terminal window on your Mac, and run the following command: `/usr/bin/env python3 -c "$(curl -fsSL https://raw.githubusercontent.com/nicolaswehmeyer/rekordbox-dropbox-library-sync/main/main.py)"`

After the script was triggered, you will be guided through the setup process. Simply follow the wizard and answer the questions according to your needs.

**After installation:**
- Once you've migrated your library to the Dropbox cloud, you can start Rekordbox and keep working as usual. Changing playlists inside of Rekordbox, tagging files etc. may lead to files being updated in the background. Be sure to have Dropbox enabled, so that all your latest changes will be replicated to your cloud
- Never open Rekordbox on two computers at the same time when using the cloud library. This could lead to race conditions and a corrupt database. Always make sure that all your latest changes were synced to your Dropbox, by closing Rekordbox and monitoring your Dropbox client to ensure all changes were synced.

## How does it work?
RDLS has several built-in checks to prevent your Rekordbox DJ Library from being removed or corrupted. It also creates backup folders of your current Rekordbox DJ Library, so you can always get to a state prior to RDLS.

Once executed, RDLS performs the follwing:
- Verification of local Dropbox installation: RDLS searches for your private Dropbox folder path by parsing the `info.json` file located under `~/.dropbox`.
- After detecting your local private Dropbox folder path, you can now specify the an existing or new Dropbox folder in which you'd like to map your local Rekordbox DJ library to
- RDLS will then check for existing Rekordbox DJ libraries within the Dropbox folder you specified, to ensure your local DJ library will not overwrite an already existing and migrated Rekordbox DJ Library
- Once you confirmed the migration process, RDLS will start moving your local files and folders to the specified Dropbox folder and then link your Dropbox based Rekordbox DJ Library back into `~/Library/Pioneer` by creating symlinks
- Once the migration was successfull, Rekordbox DJ will not be aware of the changes as the symlinks still allow Rekordbox to parse the database, playlists etc. as it normally does