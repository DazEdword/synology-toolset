#!/bin/bash
# This script is intended to be run with root privileges
# Torrent variable can be either url to torrent file or magnet

# Making sure that synopkg command will be available in path
PATH=$PATH:/usr/syno/bin/

set -e

connection=$1

if [ -z "$connection" ]; then
	echo "Missing connection details."
	exit 1
fi

# Ensure Deluge is running
status=$(synopkg status deluge)
if [[ $status == *"stopped"* ]]; then
	echo "Starting deluge..."
    synopkg start deluge
else
	echo "Deluge is already running!"
fi

# Validate Deluge Console arguments
user=$2
pass=$3

if [ -z "$user" ] || [ -z "$pass" ]; then
	echo "Missing user and/or password arguments."
	exit 1
else
    echo "Found credentials for user $user"
fi

# Validate download torrent argument
torrent=$4

if [[ -n "$torrent" ]]; then
	echo "Preparing to download: $torrent"
else
	echo "No torrent was provided. Aborting download."
	exit 1
fi

# Connect to Deluge Console
commands="connect "$connection" "$user" "$pass"; add "$torrent""
/var/packages/deluge/target/env/bin/deluge-console "$commands"

# TODO Passing passwords as parameters is bad practice, research alternatives
