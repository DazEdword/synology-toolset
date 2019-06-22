from constants import (
    DELUGE_USERNAME_NAME,
    DELUGE_PASSWORD_NAME,
    SYNOLOGY_IP_NAME,
    SYNOLOGY_USERNAME_NAME,
    SYNOLOGY_PORT_NAME,
)
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
        print(result)
    except Exception as e:
        print(e)
