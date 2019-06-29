# from unittest.mock import patch

from synotools.commands.install import build_destination_paths


def test_uses_provided_config_username_when_provided():
    username = "edword"

    sftp_path, absolute_path = build_destination_paths(username)

    assert username in sftp_path
    assert username in absolute_path


def test_returns_processed_sftp_path_as_first_element_of_tuple():
    username = "edword"

    sftp_path, absolute_path = build_destination_paths(username)

    assert sftp_path == "homes/edword/.scripts"


def test_returns_processed_absolute_path_as_second_element_of_tuple():
    username = "edword"

    sftp_path, absolute_path = build_destination_paths(username)

    assert absolute_path == "/var/services/homes/edword/.scripts"
