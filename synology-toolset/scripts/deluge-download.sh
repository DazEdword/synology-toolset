#!/bin/bash
# This script is intended to be run with root privileges

# Validate download magnet argument
magnet=$1

if [[ "$magnet" -gt "-1" ]]; then
	echo "Preparing to download magnet: $magnet"
else
	echo "No magnet was provided. Aborting download."
	exit
fi

# Ensure Deluge is running
status=$(synopkg status deluge)
if [[ $status == *"stopped"* ]]; then
    synopkg start deluge
else
	echo "Deluge is already running!"
fi

# Validate Deluge Console arguments
user=$2
pass=$3

if [ -z "$user" ] || [ -z "$pass" ]; then
	echo "Missing user and/or password arguments."
	exit
else
    echo "Found credentials for user $user"
fi

# Connect to Deluge Console
# TODO Fix that hardcoded connection!
# TODO Change pause/resume with add + magnet

commands="connect 127.0.0.1:58846 "$user" "$pass"; pause *"

/var/packages/deluge/target/env/bin/deluge-console "$commands"
