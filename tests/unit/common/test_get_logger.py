from unittest.mock import patch

from synotools.common.logging import get_logger


@patch("synotools.common.logging.logging")
def test_passes_module_name_to_instanced_logger(python_logging_mock):
    get_logger("potato.mod")

    python_logging_mock.getLogger.assert_called_once_with("potato.mod")


@patch("synotools.common.logging.PasswordMaskingFilter")
@patch("synotools.common.logging.logging")
def test_installs_password_filter(python_logging_mock, password_filter_mock):
    logger_mock = get_logger("potato.mod")

    logger_mock.addFilter.assert_called_once_with(password_filter_mock.return_value)
