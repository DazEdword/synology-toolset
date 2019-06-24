import logging

from constants import (
    DELUGE_USERNAME_NAME,
    DELUGE_PASSWORD_NAME,
    SYNOLOGY_IP_NAME,
    SYNOLOGY_USERNAME_NAME,
    SYNOLOGY_PORT_NAME,
)
from logging import Logger
from fabric import Connection

from settings import get_environmental_variable


def download_torrent_with_deluge():
    host = get_environmental_variable(SYNOLOGY_IP_NAME)
    user = get_environmental_variable(SYNOLOGY_USERNAME_NAME)

    connection = Connection(
        host=host, user=user,
    )

    try:
        result = connection.run(".scripts/hello-world.sh")
        logging.info(result)
    except Exception as e:
        logging.error("An error occurred: {e}")
