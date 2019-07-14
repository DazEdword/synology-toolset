from synotools.models.config import DelugeConfig


def test_deluge_config_initialisation_has_correct_prefix():
    actual = DelugeConfig()

    expected = "DELUGE"
    assert actual._config_prefix == expected


def test_deluge_config_initialisation_has_correct_fields():
    actual = DelugeConfig().FIELDS

    assert len(actual) == 4
    assert actual == ["username", "password", "port", "ip"]
