import argparse
import sys

from fabric import Config, Connection

from synotools.commands.constants import VPN_CONNECTED_SUBSTRING
from synotools.common.logging import get_logger
from synotools.models.config import SynoConfig, VpnConfig

logger = get_logger(__name__)


def check_and_connect():
    logger.debug("Checking VPN connection...")
    syno_config = SynoConfig()

    fabric_config = Config(overrides={"sudo": {"password": syno_config.password}})

    connection = Connection(
        host=syno_config.ip, user=syno_config.username, config=fabric_config
    )

    vpn_connected = is_vpn_enabled(connection)

    if not vpn_connected:
        connect_vpn(connection)


def is_vpn_enabled(connection):
    try:
        command = ".scripts/vpn-check-connection.sh"
        vpn_check_result = connection.sudo(command, warn=True)
        logger.info(vpn_check_result)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

    return (
        True if vpn_check_result.stdout.startswith(VPN_CONNECTED_SUBSTRING) else False
    )


def connect_vpn(connection):
    vpn_config = VpnConfig()
    params = f"{vpn_config.id} {vpn_config.name} {vpn_config.protocol}"

    try:
        command = f".scripts/vpn-connect.sh {params}"
        vpn_connect_result = connection.sudo(command, warn=True)
        logger.info(vpn_connect_result)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    check_and_connect()
