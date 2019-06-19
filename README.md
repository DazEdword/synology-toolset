# Synology Playground

A Python API wrapper and toolset for interfacing with Synology NAS devices using DiskStation Manager (DSM).

## Getting started

### Credentials

Valid credentials are expected to be stored locally, allowing the tools to connect to the device via local network. Create a new `.env.private` file by copying `.env.sample`, and add your own credentials as required:

1. IP: E.g. 192.168.1.35
2. Port: 5000 for http, and 5001 for https
3. Username: Same username you normally use to log in through the web interface
4. Password: Corresponding password

Finding out your local IP will depend on your OS, router configuration and other factors. Please refer to [DSM's User Guide](https://global.download.synology.com/download/Document/UserGuide/DSM/6.2/Syno_UsersGuide_NAServer_enu.pdf) for more details on how to get or set your device's IP.

*Note: Fore security reasons remember not share your personal credentials file or password! Do not commit to repo, or share it with anybody. That file should be private and stored safely, localy.*


## Compatibility
Tested with Synology's DS218j model.

