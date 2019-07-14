from unittest.mock import Mock

from synotools.common.logging import get_logger, PasswordMaskingFilter
from synotools.models.config import ConfigBase, SynoConfig

from tests.unit.fixtures import create_syno_config_fake

logger = get_logger(__name__)


def test_filters_config_objects_to_redact_passwords():
    log_filter = PasswordMaskingFilter()
    config = create_syno_config_fake()
    record_mock = Mock(args=config)

    actual = log_filter.filter(record_mock)

    assert actual is True  # Filter worked
    assert record_mock.args.password == "********"


def test_filters_do_not_modify_original_objects():
    log_filter = PasswordMaskingFilter()
    config = create_syno_config_fake()
    record_mock = Mock(args=config)

    log_filter.filter(record_mock)

    assert record_mock.args.password == "********"
    assert config.password == "password_mock"


def test_filters_do_not_fail_when_password_field_is_missing():
    log_filter = PasswordMaskingFilter()
    config = ConfigBase()
    record_mock = Mock(args=config)

    actual = log_filter.filter(record_mock)

    assert actual is True
    assert getattr(config, "password", None) is None
    assert getattr(record_mock.args, "password", None) is None


def test_sanitization_passes_with_objects_other_than_configs():
    log_filter = PasswordMaskingFilter()

    actual = log_filter.sanitize_config("Hello")

    assert actual == "Hello"
