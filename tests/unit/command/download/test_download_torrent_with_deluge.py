from unittest.mock import patch, Mock

from commands.download import download_torrent_with_deluge


@patch("commands.download.Connection")
@patch("commands.download.get_environmental_variable")
def test_gets_host_details(get_environmental_variable_mock, *_):
    actual = download_torrent_with_deluge()

    assert get_environmental_variable_mock.call_args_list[0][0][0] == "SYNOLOGY_IP"


@patch("commands.download.Connection")
@patch("commands.download.get_environmental_variable")
def test_gets_username_details(get_environmental_variable_mock, *_):
    actual = download_torrent_with_deluge()

    assert get_environmental_variable_mock.call_args_list[1][0][0] == "SYNOLOGY_USERNAME"


@patch("commands.download.get_environmental_variable", side_effect=["host_mock", "user_mock"])
@patch("commands.download.Connection")
def test_creates_fabric_connection_with_correct_details(connection_mock, *_):
    actual = download_torrent_with_deluge()

    connection_mock.assert_called_once_with(host="host_mock", user="user_mock")
