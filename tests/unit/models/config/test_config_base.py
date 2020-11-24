from unittest.mock import patch

from synotools.models.config.base import ConfigBase


@patch("synotools.models.config.base.logging")
def test_config_base_initialisation_logs_message_when_config_prefix_is_not_set(
    logging_mock,
):
    # Act
    ConfigBase()

    logging_mock.warning.assert_called_once_with(
        "A config prefix is required to instance ConfigBase"
    )


@patch("synotools.models.config.base.setattr")
@patch("synotools.models.config.base.Settings.get_environmental_variable")
def test_config_base_initialisation_get_fields_from_config_when_prefix_is_set(
    get_environmental_variable_mock, setattr_mock
):
    # Act
    with patch.object(ConfigBase, "_config_prefix", "TEST_CONFIG_PREFIX"):
        with patch.object(ConfigBase, "FIELDS", ["field_1", "field_2"]):
            ConfigBase()

            assert get_environmental_variable_mock.call_count == 2
            assert (
                get_environmental_variable_mock.call_args_list[0][0][0]
                == "TEST_CONFIG_PREFIX_FIELD_1"
            )
            assert (
                get_environmental_variable_mock.call_args_list[1][0][0]
                == "TEST_CONFIG_PREFIX_FIELD_2"
            )


@patch("synotools.models.config.base.Settings.get_environmental_variable")
def test_get_field_from_config_gets_fields_using_attr_name_and_config_prefix(
    get_environmental_variable_mock,
):
    config = ConfigBase()

    expected = "TEST_CONFIG_PREFIX_FIELD_1"
    config.get_field_from_config("TEST_CONFIG_PREFIX", "FIELD_1")

    get_environmental_variable_mock.assert_called_once_with(expected)
