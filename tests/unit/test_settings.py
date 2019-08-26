from synotools.settings import Settings


def test_get_environmental_variable_loads_credentials_from_expected_location(mocker):

    mocker.patch(
        "synotools.settings.Settings.get_local_credentials_path",
        "home/test-user/.my-test/credentials",
    )

    load_dotenv_mock = mocker.patch("synotools.settings.load_dotenv")

    Settings()

    load_dotenv_mock.assert_called_once_with(
        dotenv_path="home/test-user/.my-test/credentials", verbose=True
    )
