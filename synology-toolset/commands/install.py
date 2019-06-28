import logging
import os

from common.utils import zip_folder
from models.config.syno import SynoConfig
from fabric import Connection, Config

SCRIPTS_PATH = "synology-toolset/scripts"
ZIP_DESTINATION_PATH = "artifacts"

REMOTE_SFTP_DESTINATION_PATH = "homes/edword/.scripts"
REMOTE_ABSOLUTE_DESTINATION_PATH = "/var/services/homes/edword/.scripts"

def install_scripts():
    syno_config = SynoConfig()

    fabric_config = Config(overrides={"sudo": {"password": syno_config.password}})

    connection = Connection(
        host=syno_config.ip, user=syno_config.username, config=fabric_config
    )

    zipped_scripts = zip_folder('synology-scripts', SCRIPTS_PATH, ZIP_DESTINATION_PATH)

    try:
        # Ensure dir is there
        connection.run(f'mkdir -p {REMOTE_SFTP_DESTINATION_PATH}')

        # Send zipped files
        result = connection.put(
            zipped_scripts, 
            remote=REMOTE_SFTP_DESTINATION_PATH)
        logging.debug(result)



        remote_filename = os.path.join(REMOTE_ABSOLUTE_DESTINATION_PATH, os.path.basename(zipped_scripts))
        print(remote_filename)
        # Unzip
        connection.run(f'7z e {remote_filename} -o/{REMOTE_ABSOLUTE_DESTINATION_PATH} -aoa')

        # Remove zip
        connection.run(f'rm {remote_filename}')

    except Exception as e:
        logging.error(f"An error occurred: {e}")

