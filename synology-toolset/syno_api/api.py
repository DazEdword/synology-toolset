
from constants import (
    SYNOLOGY_IP_NAME,
    SYNOLOGY_PASSWORD_NAME,
    SYNOLOGY_PORT_NAME,
    SYNOLOGY_USERNAME_NAME,
)
from settings import get_environmental_variable

from SynologyDSM import SynologyDSM


def create_api_client():
    print("Creating Valid API Client")
    client = SynologyDSM(
        get_environmental_variable(SYNOLOGY_IP_NAME),
        get_environmental_variable(SYNOLOGY_PORT_NAME),
        get_environmental_variable(SYNOLOGY_USERNAME_NAME),
        get_environmental_variable(SYNOLOGY_PASSWORD_NAME),
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
