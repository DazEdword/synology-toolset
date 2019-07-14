#!/bin/bash

set -e

NOT_CONNECTED_MESSAGE="No connection!!"

echo "Checking VPN connection..."
result=$(synovpnc get_conn || /usr/syno/bin/synovpnc get_conn)

if [[ $result == *"$NOT_CONNECTED_MESSAGE"* ]]; then
	echo "VPN is not connected."
else
	echo "VPN connected: $result"
fi