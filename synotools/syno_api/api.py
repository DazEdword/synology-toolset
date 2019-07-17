from SynologyDSM import SynologyDSM

from synotools.models.config import SynoConfig
from synotools.settings import get_environmental_variable


def create_api_client():
    print("Creating Valid API Client")

    syno_config = SynoConfig()

    client = SynologyDSM(
        syno_config.ip, syno_config.port, syno_config.username, syno_config.password
    )

    return client


def print_sanity_test_report(client):
    print("=== Utilisation ===")
    print("CPU Load:   " + str(client.utilisation.cpu_total_load) + " %")
    print("Memory Use: " + str(client.utilisation.memory_real_usage) + " %")
    print("Net Up:     " + str(client.utilisation.network_up()))
    print("Net Down:   " + str(client.utilisation.network_down()))

    print("=== Storage ===")
    volumes = client.storage.volumes
    for volume in volumes:
        print("ID:         " + str(volume))
        print("Status:     " + str(client.storage.volume_status(volume)))
        print(
            "% Used:     " + str(client.storage.volume_percentage_used(volume)) + " %"
        )

    disks = client.storage.disks
    for disk in disks:
        print("ID:         " + str(disk))
        print("Name:       " + str(client.storage.disk_name(disk)))
        print("S-Status:   " + str(client.storage.disk_smart_status(disk)))
        print("Status:     " + str(client.storage.disk_status(disk)))
        print("Temp:       " + str(client.storage.disk_temp(disk)))
