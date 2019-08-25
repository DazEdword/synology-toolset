from unittest.mock import Mock, patch

from synotools.commands.install import run_remote_installation_commands
from tests.unit.fixtures import create_syno_config_mock


"""
Note: Since connection is handled with a context manager, many assertions
in this test file occur against mock_calls. This pattern should not be used
unless it's absolutely necessary, use mock.assert_called_with instead.
"""


@patch("synotools.commands.install.os.path")
@patch("synotools.commands.install.Connection")
@patch("synotools.commands.install.Config")
def test_opens_fabric_connection_with_correct_credentials(
    config_mock, connection_mock, *_
):
    syno_config = create_syno_config_mock()
    run_remote_installation_commands(syno_config, Mock(), "", "")

    config_mock.assert_called_once_with(
        overrides={"sudo": {"password": "password_mock"}}
    )

    connection_mock.assert_called_once_with(
        host="host_mock", user="user_mock", config=config_mock.return_value
    )


@patch("synotools.commands.install.os.path")
@patch("synotools.commands.install.Config")
@patch("synotools.commands.install.Connection")
def test_creates_scripts_dir_in_destination_if_it_does_not_exist(connection_mock, *_):
    syno_config = create_syno_config_mock()
    run_remote_installation_commands(syno_config, Mock(), "/example/path", "")

    mock_methods = [calls[0] for calls in connection_mock.mock_calls]
    mock_calls = [calls[1] for calls in connection_mock.mock_calls]

    assert "run" in mock_methods[2]
    assert "mkdir -p /example/path" in mock_calls[2]


@patch("synotools.commands.install.os.path")
@patch("synotools.commands.install.Config")
@patch("synotools.commands.install.Connection")
def test_creates_transfers_zipped_files(connection_mock, *_):
    syno_config = create_syno_config_mock()
    run_remote_installation_commands(
        syno_config,
        "/local/zipped/files.zip",
        "/example/path",
        "/absolute/example/path",
    )

    mock_methods = [calls[0] for calls in connection_mock.mock_calls]
    mock_args = [args for args in connection_mock.mock_calls]

    assert "put" in mock_methods[3]
    assert "/local/zipped/files.zip" in mock_args[3][1]
    assert {"remote": "/example/path"} == mock_args[3][2]


@patch("synotools.commands.install.Config")
@patch("synotools.commands.install.os.path")
@patch("synotools.commands.install.Connection")
def test_runs_unzip_command_on_destination(connection_mock, os_path_mock, *_):
    os_path_mock.join.return_value = "processed/path/files.zip"
    syno_config = create_syno_config_mock()
    run_remote_installation_commands(
        syno_config,
        "/local/zipped/files.zip",
        "/example/path",
        "/absolute/example/path",
    )

    mock_methods = [calls[0] for calls in connection_mock.mock_calls]
    mock_args = [args for args in connection_mock.mock_calls]

    assert "run" in mock_methods[4]
    assert (
        "7z e processed/path/files.zip -o//absolute/example/path -aoa"
        in mock_args[4][1]
    )


@patch("synotools.commands.install.Config")
@patch("synotools.commands.install.os.path")
@patch("synotools.commands.install.Connection")
def test_deleted_zipped_file_after_extraction(connection_mock, os_path_mock, *_):
    os_path_mock.join.return_value = "processed/path/files.zip"
    syno_config = create_syno_config_mock()
    run_remote_installation_commands(
        syno_config,
        "/local/zipped/files.zip",
        "/example/path",
        "/absolute/example/path",
    )

    mock_methods = [calls[0] for calls in connection_mock.mock_calls]
    mock_args = [args for args in connection_mock.mock_calls]

    assert "run" in mock_methods[5]
    assert "rm processed/path/files.zip" in mock_args[5][1]
