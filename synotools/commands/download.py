import sys

from fabric import Config, Connection

from synotools.common.logging import get_logger
from synotools.models.config import DelugeConfig, SynoConfig

logger = get_logger(__name__)


def download_torrent_with_deluge(torrent_url):
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

    try:
        torrent_url = sys.argv[1]
    except IndexError:
        pass

    download_torrent_with_deluge(torrent_url)
