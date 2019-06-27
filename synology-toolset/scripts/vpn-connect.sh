#!/bin/sh

# TODO Hardcoded config details, needs to be passed
ID=o1558979999

cat >/usr/syno/etc/synovpnclient/vpnc_connecting <<END
conf_id=$ID
conf_name=NordVPN_UK75
proto=openvpn
END

synovpnc connect --id=$ID