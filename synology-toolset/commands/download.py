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
from logging import Logger
from fabric import Connection, Config
from invoke import Responder

from settings import get_environmental_variable


def download_torrent_with_deluge(torrent_url):
    host = get_environmental_variable(SYNOLOGY_IP_NAME)
    user = get_environmental_variable(SYNOLOGY_USERNAME_NAME)
    password = get_environmental_variable(SYNOLOGY_PASSWORD_NAME)

    deluge_ip = get_environmental_variable(DELUGE_IP_NAME)
    deluge_port = get_environmental_variable(DELUGE_PORT_NAME)
    deluge_connection = f"{deluge_ip}:{deluge_port}"

    deluge_user = get_environmental_variable(DELUGE_USERNAME_NAME)
    deluge_password = get_environmental_variable(DELUGE_PASSWORD_NAME)

    config = Config(overrides={"sudo": {"password": password}})

    connection = Connection(host=host, user=user, config=config)

    sudopass = Responder(pattern=r"\[sudo\] password:", response=f"{password}\n")

    try:
        command = f'.scripts/deluge-download.sh "{deluge_connection}" {deluge_user} {deluge_password} "{torrent_url}"'
        result = connection.sudo(command)
        logging.info(result)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
