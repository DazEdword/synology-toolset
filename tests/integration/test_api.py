from synotools.syno_api.api import create_api_client, print_sanity_test_report


def test_whatevs():
    client = create_api_client()

    print_sanity_test_report(client)


if __name__ == "__main__":
    test_whatevs()
