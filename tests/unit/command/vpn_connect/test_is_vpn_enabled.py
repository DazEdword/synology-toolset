from unittest.mock import Mock, patch

import pytest

from synotools.commands.constants import VPN_CONNECTED_SUBSTRING
from synotools.commands.vpn_connect import is_vpn_enabled


@patch("synotools.commands.vpn_connect.logger")
def test_calls_vpn_connection_check_script_via_open_fabric_connection(logger_mock):
    connection_mock = Mock()
    connection_mock.sudo.return_value.stdout = "Command output."

    is_vpn_enabled(connection_mock)

    expected_command = ".scripts/vpn-check-connection.sh"
    connection_mock.sudo.assert_called_once_with(expected_command, warn=True)


@patch("synotools.commands.vpn_connect.logger")
def test_returns_true_when_vpn_is_active(logger_mock,):
    connection_mock = Mock()
    connection_mock.sudo.return_value.stdout = (
        f"{VPN_CONNECTED_SUBSTRING} Extra command output."
    )

    actual = is_vpn_enabled(connection_mock)

    assert actual is True


@patch("synotools.commands.vpn_connect.logger")
def test_returns_false_when_vpn_is_not_active(logger_mock,):
    connection_mock = Mock()
    connection_mock.sudo.return_value.stdout = f"Not very connected command output."

    actual = is_vpn_enabled(connection_mock)

    assert actual is False


@patch("synotools.commands.vpn_connect.logger")
def test_raises_exception_when_command_fails(logger_mock,):
    connection_mock = Mock()
    connection_mock.sudo.side_effect = [Exception("Derp.")]

    with pytest.raises(Exception):
        is_vpn_enabled(connection_mock)
        logger_mock.error.assert_called_once_with("An error occurred: Derp.")
