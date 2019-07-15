from unittest.mock import Mock, patch

import pytest

from synotools.commands.constants import VPN_CONNECTED_SUBSTRING
from synotools.commands.vpn_connect import connect_vpn
from tests.unit.fixtures import create_syno_config_mock, create_vpn_config_fake


@patch("synotools.commands.vpn_connect.logger")
@patch(
    "synotools.commands.vpn_connect.VpnConfig", return_value=create_vpn_config_fake()
)
def test_calls_vpn_connection_check_script_via_open_fabric_connection(*_,):
    connection_mock = Mock()

    connect_vpn(connection_mock)

    expected_command = ".scripts/vpn-connect.sh 0123456789 vpn-fake-name openvpn"
    connection_mock.sudo.assert_called_once_with(expected_command)


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
