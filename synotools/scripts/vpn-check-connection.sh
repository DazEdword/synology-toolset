#!/bin/bash

set -e

NOT_CONNECTED_MESSAGE="No connection!!"

echo "Checking VPN connection..."

if hash synovpnc 2>/dev/null; then
	result=$(synovpnc get_conn)
elif hash /usr/syno/bin/synovpnc 2>/dev/null; then
	result=$(/usr/syno/bin/synovpnc get_conn)
fi

if [[ $result == *"$NOT_CONNECTED_MESSAGE"* ]]; then
	echo "VPN is not connected."
else
	echo "VPN connected: $result"
fi