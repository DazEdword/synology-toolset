from unittest.mock import patch, Mock

from commands.download import download_torrent_with_deluge
from tests.unit.fixtures import create_syno_config_mock

TORRENT_URL = "https://www.archlinux.org/releng/releases/2019.06.01/torrent/"


@patch("commands.download.Connection")
@patch("commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("commands.download.get_environmental_variable")
def test_gets_synology_config_details(
    get_environmental_variable_mock, syno_config_mock, *_
):
    actual = download_torrent_with_deluge(TORRENT_URL)
    syno_config_mock.assert_called_once()


@patch("commands.download.logging")
@patch(
    "commands.download.get_environmental_variable",
    side_effect=[
        "deluge_ip_mock",
        "deluge_port_mock",
        "deluge_connection_mock",
        "deluge_user_mock",
        "deluge_password_mock",
    ],
)
@patch("commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("commands.download.Config")
@patch("commands.download.Connection")
def test_creates_fabric_connection_with_correct_sudo_config(
    connection_mock, config_mock, *_
):
    actual = download_torrent_with_deluge(TORRENT_URL)

    config_mock.assert_called_once_with(
        overrides={"sudo": {"password": "password_mock"}}
    )


@patch("commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("commands.download.logging")
@patch(
    "commands.download.get_environmental_variable",
    side_effect=[
        "deluge_ip_mock",
        "deluge_port_mock",
        "deluge_connection_mock",
        "deluge_user_mock",
        "deluge_password_mock",
    ],
)
@patch("commands.download.SynoConfig", return_value=create_syno_config_mock())
@patch("commands.download.Config")
@patch("commands.download.Connection")
def test_creates_fabric_connection_with_correct_credentials(
    connection_mock, config_mock, *_
):
    actual = download_torrent_with_deluge(TORRENT_URL)

    connection_mock.assert_called_once_with(
        host="host_mock", user="user_mock", config=config_mock.return_value
    )
    expected_command = '.scripts/deluge-download.sh "deluge_ip_mock:deluge_port_mock" deluge_connection_mock deluge_user_mock "https://www.archlinux.org/releng/releases/2019.06.01/torrent/"'
    connection_mock.return_value.sudo.assert_called_once_with(expected_command)
