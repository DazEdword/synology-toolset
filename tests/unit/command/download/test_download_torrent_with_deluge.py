from unittest.mock import patch

from synotools.commands.download import download_torrent_with_deluge
from tests.unit.fixtures import (create_deluge_config_mock,
                                 create_syno_config_mock)

TORRENT_URL = "https://www.archlinux.org/releng/releases/2019.06.01/torrent/"


@patch("synotools.commands.download.Connection")
@patch(
    "synotools.commands.download.DelugeConfig", return_value=create_deluge_config_mock()
)
@patch("synotools.commands.download.SynoConfig", return_value=create_syno_config_mock())
def test_gets_synology_config_details(syno_config_mock, deluge_config_mock, *_):
    download_torrent_with_deluge(TORRENT_URL)
    syno_config_mock.assert_called_once()


@patch("synotools.commands.download.Connection")
@patch("synotools.commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch(
    "synotools.commands.download.DelugeConfig", return_value=create_deluge_config_mock()
)
def test_gets_deluge_config_details(deluge_config_mock, *_):
    download_torrent_with_deluge(TORRENT_URL)
    deluge_config_mock.assert_called_once()


@patch("synotools.commands.download.get_logger")
@patch(
    "synotools.commands.download.DelugeConfig", return_value=create_deluge_config_mock()
)
@patch("synotools.commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("synotools.commands.download.Config")
@patch("synotools.commands.download.Connection")
def test_creates_fabric_connection_with_correct_sudo_config(
    connection_mock, config_mock, *_
):
    download_torrent_with_deluge(TORRENT_URL)

    config_mock.assert_called_once_with(
        overrides={"sudo": {"password": "password_mock"}}
    )


@patch("synotools.commands.download.logger")
@patch(
    "synotools.commands.download.DelugeConfig", return_value=create_deluge_config_mock()
)
@patch("synotools.commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("synotools.commands.download.Config")
@patch("synotools.commands.download.Connection")
def test_creates_fabric_connection_with_correct_credentials(
    connection_mock, config_mock, *_
):
    download_torrent_with_deluge(TORRENT_URL)

    connection_mock.assert_called_once_with(
        host="host_mock", user="user_mock", config=config_mock.return_value
    )
    expected_command = '.scripts/deluge-download.sh "deluge_service_host_mock:8888" deluge_user_mock deluge_password_mock "https://www.archlinux.org/releng/releases/2019.06.01/torrent/"'  # noqa: E501
    connection_mock.return_value.sudo.assert_called_once_with(expected_command)


@patch(
    "synotools.commands.download.DelugeConfig", return_value=create_deluge_config_mock()
)
@patch("synotools.commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("synotools.commands.download.Config")
@patch("synotools.commands.download.logger")
@patch("synotools.commands.download.Connection")
def test_logs_message_when_exception_occurs(connection_mock, logger_mock, *_):
    connection_mock.return_value.sudo.side_effect = [
        Exception("Uh oh, something happened!")
    ]

    download_torrent_with_deluge(TORRENT_URL)

    logger_mock.error.assert_called_once_with(
        f"An error occurred: Uh oh, something happened!"
    )
