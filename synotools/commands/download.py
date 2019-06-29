import logging

from fabric import Connection, Config

from synotools.models.config.syno import SynoConfig
from synotools.models.config.deluge import DelugeConfig


def download_torrent_with_deluge(torrent_url):
    syno_config = SynoConfig()
    deluge_config = DelugeConfig()

    deluge_connection = f"{deluge_config.ip}:{deluge_config.port}"

    fabric_config = Config(overrides={"sudo": {"password": syno_config.password}})

    connection = Connection(
        host=syno_config.ip, user=syno_config.username, config=fabric_config
    )

    try:
        command = f'.scripts/deluge-download.sh "{deluge_connection}" {deluge_config.username} {deluge_config.password} "{torrent_url}"'
        result = connection.sudo(command)
        logging.info(result)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
