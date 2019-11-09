import argparse

from fabric import Config, Connection

from synotools.commands.vpn_connect import check_and_connect
from synotools.common.logging import get_logger
from synotools.models.config import DelugeConfig, SynoConfig

logger = get_logger(__name__)


def download_torrent_with_deluge(torrent_url, skip_vpn=False):
    if skip_vpn:
        logger.info("Skipping VPN checks...")
    else:
        check_and_connect()

    logger.debug("Creating config files...")
    syno_config = SynoConfig()
    deluge_config = DelugeConfig()

    deluge_connection = f"{deluge_config.ip}:{deluge_config.port}"

    fabric_config = Config(overrides={"sudo": {"password": syno_config.password}})

    connection = Connection(
        host=syno_config.ip, user=syno_config.username, config=fabric_config
    )

    try:
        command = '.scripts/deluge-download.sh "{d_conn}" {d_user} {d_password} "{torrent_url}"'.format(
            d_conn=deluge_connection,
            d_user=deluge_config.username,
            d_password=deluge_config.password,
            torrent_url=torrent_url,
        )

        result = connection.sudo(command)
        logger.info(result)
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    torrent_url = None

    parser = argparse.ArgumentParser(description="Download torrent with Deluge.")
    parser.add_argument(
        "torrent_url", type=str, help="the torrent url or magnet to download"
    )
    parser.add_argument(
        "--no-vpn",
        dest="no_vpn",
        action="store_true",
        help="skip vpn check and/or vpn connection (if disabled)",
        required=False,
    )

    args = parser.parse_args()
    torrent_url = args.torrent_url
    no_vpn = args.no_vpn

    download_torrent_with_deluge(torrent_url, no_vpn)
