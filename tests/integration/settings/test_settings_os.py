from synotools.settings import Settings


class TestSettingsOS:
    def test_get_environmental_variable_loads_credentials_from_expected_location_on_linux(
        self, mocker,
    ):
        # Arrange
        mocker.patch("synotools.settings.sys.platform", "linux")

        # Act
        target = Settings()

        actual = target.credentials_path

        # Assert
        assert actual.endswith("credentials")

    def test_get_environmental_variable_loads_credentials_from_expected_location_on_windows(
        self, mocker,
    ):
        # Arrange
        mocker.patch("synotools.settings.sys.platform", "win32")

        # Act
        target = Settings()

        actual = target.credentials_path

        # Assert
        assert actual.endswith("credentials.txt")
