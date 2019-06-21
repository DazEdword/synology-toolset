from src.api import create_api_client, print_sanity_test_report


def test_whatevs():
    client = create_api_client()

    print_sanity_test_report(client)
