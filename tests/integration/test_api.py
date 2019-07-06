import pytest

from synotools.syno_api.api import create_api_client, print_sanity_test_report

# Ensure this test module is seen as an integration test
pytestmark = pytest.mark.integration

# TODO Requires real access, redesign .env handling
# def test_print_sanity_test_report():
#     client = create_api_client()

#     print_sanity_test_report(client)
