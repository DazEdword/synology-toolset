#!/bin/sh

NOT_CONNECTED_MESSAGE="No connection!!"

echo "Checking VPN connection..."

result=$(synovpnc get_conn)

if [[ $result == *"$NOT_CONNECTED_MESSAGE"* ]]; then
	echo "VPN is not connected."
else
	echo "VPN connected:"
	echo $result
fi