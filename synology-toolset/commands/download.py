import logging

from constants import (
    DELUGE_USERNAME_NAME,
    DELUGE_PASSWORD_NAME,
    SYNOLOGY_IP_NAME,
    SYNOLOGY_USERNAME_NAME,
    SYNOLOGY_PASSWORD_NAME,
)
from logging import Logger
from fabric import Connection
from invoke import Responder

from settings import get_environmental_variable


def download_torrent_with_deluge():
    host = get_environmental_variable(SYNOLOGY_IP_NAME)
    user = get_environmental_variable(SYNOLOGY_USERNAME_NAME)
    password = get_environmental_variable(SYNOLOGY_PASSWORD_NAME)

    connection = Connection(
        host=host, user=user,
    )

    sudopass = Responder(
        pattern=r'\[sudo\] password:',
        response=f'{password}\n',
    )

    try:
        result = connection.run("sudo .scripts/deluge-download.sh", watchers=[sudopass])
        logging.info(result)
    except Exception as e:
        logging.error("An error occurred: {e}")
