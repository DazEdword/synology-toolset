from synotools.models.config import VpnConfig


def test_syno_config_initialisation_has_correct_prefix():
    actual = VpnConfig()

    expected = "VPN"
    assert actual._config_prefix == expected


def test_syno_config_initialisation_has_correct_fields():
    actual = VpnConfig().FIELDS

    assert len(actual) == 3
    assert actual == ["id", "name", "protocol"]
