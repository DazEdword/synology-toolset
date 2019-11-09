from unittest.mock import patch

from synotools.commands.vpn_connect import check_and_connect
from tests.unit.fixtures import create_syno_config_mock


@patch("synotools.commands.vpn_connect.Connection")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
def test_gets_synology_config_details(syno_config_mock, deluge_config_mock, *_):
    check_and_connect()
    syno_config_mock.assert_called_once()


@patch("synotools.commands.vpn_connect.get_logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.Connection")
def test_creates_fabric_connection_with_correct_sudo_config(
    connection_mock, config_mock, *_
):
    check_and_connect()

    config_mock.assert_called_once_with(
        overrides={"sudo": {"password": "password_mock"}}
    )


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.Connection")
def test_creates_fabric_connection_with_correct_credentials(
    connection_mock, config_mock, *_
):
    check_and_connect()

    connection_mock.assert_called_once_with(
        host="host_mock", user="user_mock", config=config_mock.return_value
    )


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.is_vpn_enabled")
@patch("synotools.commands.vpn_connect.Connection")
def test_checks_whether_vpn_connection_is_already_being_used(
    connection_mock, is_vpn_enabled_mock, *_
):
    check_and_connect()

    is_vpn_enabled_mock.assert_called_once_with(connection_mock.return_value)


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.connect_vpn")
@patch("synotools.commands.vpn_connect.is_vpn_enabled")
@patch("synotools.commands.vpn_connect.Connection")
def test_does_not_connect_if_already_connected(
    connection_mock, is_vpn_enabled_mock, connect_vpn_mock, *_
):
    is_vpn_enabled_mock.return_value = True

    check_and_connect()

    connect_vpn_mock.assert_not_called()


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.connect_vpn")
@patch("synotools.commands.vpn_connect.is_vpn_enabled")
@patch("synotools.commands.vpn_connect.Connection")
def test_connects_if_check_retrieves_it_is_not_connected(
    connection_mock, is_vpn_enabled_mock, connect_vpn_mock, *_
):
    is_vpn_enabled_mock.return_value = False

    check_and_connect()

    connect_vpn_mock.assert_called_once_with(connection_mock.return_value)


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.connect_vpn")
@patch("synotools.commands.vpn_connect.is_vpn_enabled")
@patch("synotools.commands.vpn_connect.Connection")
def test_returns_true_when_vpn_is_already_connected(
    connection_mock, is_vpn_enabled_mock, connect_vpn_mock, *_
):
    # Arrange
    is_vpn_enabled_mock.return_value = True

    # Act
    actual = check_and_connect()

    # Assert
    assert actual is True
    assert not connect_vpn_mock.called


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock()
)
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.connect_vpn")
@patch("synotools.commands.vpn_connect.is_vpn_enabled")
@patch("synotools.commands.vpn_connect.Connection")
def test_returns_true_when_vpn_is_attempted_to_connect_and_succeeds(
    connection_mock, is_vpn_enabled_mock, connect_vpn_mock, *_
):
    # Arrange
    is_vpn_enabled_mock.return_value = False
    connect_vpn_mock.return_value = True

    # Act
    actual = check_and_connect()

    # Assert
    assert actual is True
    connect_vpn_mock.assert_called_once_with(connection_mock.return_value)
