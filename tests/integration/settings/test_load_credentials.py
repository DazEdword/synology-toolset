from synotools.settings import get_environmental_variable


# TODO Fix this with integration tests
# Needs to load from .env.tests instead
def test_get_environmental_variable_loads_credentials_from_expected_location():
    """Loads from ~/.synotools/credentials"""
    actual = get_environmental_variable("SYNOLOGY_IP")

    assert actual == "192.168.1.68"
