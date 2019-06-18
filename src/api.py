from constants import (
    SYNOLOGY_IP_NAME,
    SYNOLOGY_PASSWORD_NAME,
    SYNOLOGY_PORT_NAME,
    SYNOLOGY_USERNAME_NAME,
)
from settings import get_environmental_variable

from SynologyDSM import SynologyDSM

print("Creating Valid API")
api = SynologyDSM(
    get_environmental_variable(SYNOLOGY_IP_NAME),
    get_environmental_variable(SYNOLOGY_PORT_NAME),
    get_environmental_variable(SYNOLOGY_USERNAME_NAME),
    get_environmental_variable(SYNOLOGY_PASSWORD_NAME),
)

print("=== Utilisation ===")
print("CPU Load:   " + str(api.utilisation.cpu_total_load) + " %")
print("Memory Use: " + str(api.utilisation.memory_real_usage) + " %")
print("Net Up:     " + str(api.utilisation.network_up()))
print("Net Down:   " + str(api.utilisation.network_down()))

print("=== Storage ===")
volumes = api.storage.volumes
for volume in volumes:
    print("ID:         " + str(volume))
    print("Status:     " + str(api.storage.volume_status(volume)))
    print("% Used:     " + str(api.storage.volume_percentage_used(volume)) + " %")

disks = api.storage.disks
for disk in disks:
    print("ID:         " + str(disk))
    print("Name:       " + str(api.storage.disk_name(disk)))
    print("S-Status:   " + str(api.storage.disk_smart_status(disk)))
    print("Status:     " + str(api.storage.disk_status(disk)))
    print("Temp:       " + str(api.storage.disk_temp(disk)))
