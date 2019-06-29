from synotools.models.config.syno import SynoConfig


def test_syno_config_initialisation_has_correct_prefix():
    actual = SynoConfig()

    expected = "SYNOLOGY"
    assert actual._config_prefix == expected


def test_syno_config_initialisation_has_correct_fields():
    actual = SynoConfig().FIELDS

    assert len(actual) == 4
    assert actual == ["username", "password", "port", "ip"]
