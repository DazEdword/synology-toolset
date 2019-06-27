from models.config.syno import Syno


def test_syno_config_initialisation_has_correct_prefix():
    actual = Syno()

    expected = "SYNOLOGY"
    assert actual._config_prefix == expected


def test_syno_config_initialisation_has_correct_fields():
    actual = Syno().FIELDS

    assert len(actual) == 4
    assert actual ==['username', 'password', 'port', 'ip']
