import logging

from constants import (
    DELUGE_USERNAME_NAME,
    DELUGE_PASSWORD_NAME,
    DELUGE_IP_NAME,
    DELUGE_PORT_NAME,
    SYNOLOGY_IP_NAME,
    SYNOLOGY_USERNAME_NAME,
    SYNOLOGY_PASSWORD_NAME,
)

from models.config.syno import SynoConfig
from models.config.deluge import DelugeConfig
from logging import Logger
from fabric import Connection, Config
from invoke import Responder

from settings import get_environmental_variable


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
