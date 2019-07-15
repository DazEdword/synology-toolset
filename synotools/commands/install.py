import os
import sys

from fabric import Config, Connection

from synotools.common.logging import get_logger
from synotools.common.utils import zip_folder
from synotools.constants import SCRIPTS_PATH, ZIP_DESTINATION_PATH
from synotools.models.config import SynoConfig

logger = get_logger(__name__)


def install_scripts(destination_username=None):
    """
    Zips scripts from project and installs them in the NAS device through
    several fabric actions. A username can be passed to specify which user's
    home to install the scripts to. If not passed, value will be taken from
    environment config.
    """
    syno_config = SynoConfig()
    destination_username = (
        destination_username if destination_username else syno_config.username
    )

    # Build sftp and absolute paths
    remote_sftp_destination_path, remote_absolute_destination_path = build_destination_paths(
        destination_username
    )

    # Zip files
    zipped_scripts = zip_folder(
        "synology-scripts", SCRIPTS_PATH, ZIP_DESTINATION_PATH, [".py"]
    )

    try:
        run_remote_installation_commands(
            syno_config,
            zipped_scripts,
            remote_sftp_destination_path,
            remote_absolute_destination_path,
        )

    except Exception as e:
        logger.error(f"An error occurred: {e}")


def build_destination_paths(username):
    REMOTE_SFTP_DESTINATION_PATH = "homes/<username>/.scripts"
    REMOTE_ABSOLUTE_DESTINATION_PATH = "/var/services/homes/<username>/.scripts"

    return (
        REMOTE_SFTP_DESTINATION_PATH.replace("<username>", username),
        REMOTE_ABSOLUTE_DESTINATION_PATH.replace("<username>", username),
    )


def run_remote_installation_commands(
    syno_config,
    zipped_scripts,
    remote_sftp_destination_path,
    remote_absolute_destination_path,
):
    fabric_config = Config(overrides={"sudo": {"password": syno_config.password}})
    with Connection(
        host=syno_config.ip, user=syno_config.username, config=fabric_config
    ) as connection:
        # Ensure dir is there
        connection.run(f"mkdir -p {remote_sftp_destination_path}")

        # Send zipped files
        result = connection.put(zipped_scripts, remote=remote_sftp_destination_path)
        logger.debug(result)

        remote_filename = os.path.join(
            remote_absolute_destination_path, os.path.basename(zipped_scripts)
        )

        # Unzip in destination
        connection.run(
            f"7z e {remote_filename} -o/{remote_absolute_destination_path} -aoa"
        )

        # Remove zip in destination
        connection.run(f"rm {remote_filename}")


if __name__ == "__main__":
    username = None

    try:
        username = sys.argv[1]
    except IndexError:
        pass

    install_scripts(username)
