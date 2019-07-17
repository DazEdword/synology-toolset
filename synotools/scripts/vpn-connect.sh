#!/bin/sh

set -e

config_id=$1
config_name=$2
protocol=$3

if [ -z "$config_id" ] || [ -z "$config_name" ] || [ -z "$protocol" ]; then
	echo "Missing VPN configuration details."
	exit 1
fi

cat >/usr/syno/etc/synovpnclient/vpnc_connecting <<END
conf_id=$config_id
conf_name=$config_name
proto=$protocol
END


if hash synovpnc 2>/dev/null; then
	result=$(synovpnc connect --id=$config_id)
elif hash /usr/syno/bin/synovpnc 2>/dev/null; then
	result=$(/usr/syno/bin/synovpnc connect --id=$config_id)
fi

if [ $? -eq 0 ]; then
    echo "Connected to $config_name"
else
    echo "Failed to connect!"
fi
