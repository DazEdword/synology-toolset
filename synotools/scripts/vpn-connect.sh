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

synovpnc connect --id=$config_id

if [ $? -eq 0 ]; then
    echo "Connected to $config_name"
else
    echo "Failed to connect!"
fi
