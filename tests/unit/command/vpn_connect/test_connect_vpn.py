from unittest.mock import Mock, patch

import pytest

from synotools.commands.vpn_connect import connect_vpn
from tests.unit.fixtures import create_vpn_config_fake


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.VpnConfig", return_value=create_vpn_config_fake()
)
def test_calls_vpn_connection_check_script_via_open_fabric_connection(
    *_,
):
    connection_mock = Mock()

    connect_vpn(connection_mock)

    expected_command = ".scripts/vpn-connect.sh 0123456789 vpn-fake-name openvpn"
    connection_mock.sudo.assert_called_once_with(expected_command, warn=True)


@patch(
    "synotools.commands.vpn_connect.VpnConfig", return_value=create_vpn_config_fake()
)
@patch("synotools.commands.vpn_connect.logger")
def test_logs_error_ans_raises_exception_when_fabric_process_fails(logger_mock, *_):
    connection_mock = Mock()
    connection_mock.sudo.side_effect = Exception("Hah! Didn't work.")

    with pytest.raises(Exception):
        connect_vpn(connection_mock)

    logger_mock.error.assert_called_once_with("An error occurred: Hah! Didn't work.")


@patch(
    "synotools.commands.vpn_connect.VpnConfig", return_value=create_vpn_config_fake()
)
@patch("synotools.commands.vpn_connect.logger")
def test_returns_true_when_remote_script_succeeds(logger_mock, *_):
    # Arrange
    connection_mock = Mock()
    connection_mock.sudo.return_value = Mock(ok=True)

    # Act
    actual = connect_vpn(connection_mock)

    # Assert
    assert actual is True


@patch(
    "synotools.commands.vpn_connect.VpnConfig", return_value=create_vpn_config_fake()
)
@patch("synotools.commands.vpn_connect.logger")
def test_returns_false_when_remote_script_fails(logger_mock, *_):
    # Arrange
    connection_mock = Mock()
    connection_mock.sudo.return_value = Mock(ok=False)

    # Act
    actual = connect_vpn(connection_mock)

    # Assert
    assert actual is False
