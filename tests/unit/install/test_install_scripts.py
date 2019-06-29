from unittest.mock import patch

from commands.install import install_scripts
from tests.unit.fixtures import create_syno_config_mock


@patch("commands.install.SynoConfig")
@patch("commands.install.run_remote_installation_commands")
@patch("commands.install.zip_folder")
@patch(
    "commands.install.build_destination_paths",
    return_value=("/sftp/path/example", "/absolute/path/example"),
)
def test_optionally_accepts_username_as_parameter(*_):
    assert install_scripts("testuser") is None
    assert install_scripts() is None


@patch("commands.install.run_remote_installation_commands")
@patch("commands.install.zip_folder")
@patch(
    "commands.install.build_destination_paths",
    return_value=("/sftp/path/example", "/absolute/path/example"),
)
@patch("commands.install.SynoConfig")
def test_instances_required_configurations(syno_config_mock, *_):
    install_scripts()
    syno_config_mock.assert_called_once()


@patch("commands.install.run_remote_installation_commands")
@patch("commands.install.zip_folder")
@patch("commands.install.SynoConfig", return_value=create_syno_config_mock())
@patch(
    "commands.install.build_destination_paths",
    return_value=("/sftp/path/example", "/absolute/path/example"),
)
def test_builds_destination_paths_according_to_default_username(
    build_destination_paths_mock, *_
):
    install_scripts()

    build_destination_paths_mock.assert_called_once_with("user_mock")


@patch("commands.install.run_remote_installation_commands")
@patch("commands.install.zip_folder")
@patch("commands.install.SynoConfig", return_value=create_syno_config_mock())
@patch(
    "commands.install.build_destination_paths",
    return_value=("/sftp/path/example", "/absolute/path/example"),
)
def test_builds_destination_paths_according_to_username(
    build_destination_paths_mock, *_
):
    install_scripts("test_user")

    build_destination_paths_mock.assert_called_once_with("test_user")


@patch(
    "commands.install.build_destination_paths",
    return_value=("/sftp/path/example", "/absolute/path/example"),
)
@patch("commands.install.zip_folder")
@patch("commands.install.SynoConfig")
@patch("commands.install.run_remote_installation_commands")
def test_runs_remote_installation_commands(run_remote_installation_commands_mock, *_):
    install_scripts("test_user")

    run_remote_installation_commands_mock.assert_called_once()


@patch(
    "commands.install.build_destination_paths",
    return_value=("/sftp/path/example", "/absolute/path/example"),
)
@patch("commands.install.zip_folder")
@patch("commands.install.SynoConfig")
@patch(
    "commands.install.run_remote_installation_commands",
    side_effect=Exception("Something went wrong remotely!"),
)
@patch("commands.install.logging")
def test_logs_error_on_command_exception(logging_mock, *_):
    install_scripts("test_user")

    logging_mock.error.assert_called_once_with(
        "An error occurred: Something went wrong remotely!"
    )
