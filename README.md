# Synology Toolset

A Python API wrapper and toolset for interfacing with Synology NAS devices using DiskStation Manager (DSM). The repository provides two different toolsets to communicate with your NAS:

* API: Through a Python wrapper simplifying DSM queries.
* Command system: Through sh scripts hosted in the device, but called from any unix system capable of running `fabric`.

API requires valid credentials as described in the section below. Additionally, SSH access is required to run commands, optionally with the installation of SSH key-based authentication allowing the user to authenticate and operate with their NAS without constantly using a password.

## Getting started

### Credentials

Valid credentials are expected to be stored locally, allowing the tools to connect to the device via local network. Create a new `.env.private` file by copying `.env.sample`, and add your own credentials as required:

1. IP: E.g. 192.168.1.35
2. Port: 5000 for http, and 5001 for https
3. Username: Same username you normally use to log in through the web interface
4. Password: Corresponding password

Finding out your local IP will depend on your OS, router configuration and other factors. Please refer to [DSM's User Guide](https://global.download.synology.com/download/Document/UserGuide/DSM/6.2/Syno_UsersGuide_NAServer_enu.pdf) for more details on how to get or set your device's IP.

*Note: Fore security reasons remember not share your personal credentials file or password! Do not commit to repository, or share it with anybody. That file should be private and stored safely, locally.*

### Optional: SSH key

_TODO_: Add instructions

### Enabling NAS SSH access

By default terminal access is disabled in your device. Enable it as described [in the official support](https://www.synology.com/en-global/knowledgebase/SRM/help/SRM/RouterApp/admin_services#t1_1).


## Compatibility

Tested with Synology's DS218j model.

## Development

This software has been created and is maintained in Linux Mint, but developers should be able to contribute using practically any Unix platform. Before starting, the following tools will need to be installed and configured:

* Docker
* Git

### Dependencies

There are two types of dependencies:

* Python Packages: Handled automatically thanks to `pip3`. They are included in requirements file, `requirements.txt` for the tools themselves, and `requirements-dev` for all peripheric development tools. 
* Other Dependencies: In order to prevent the developers' system from cluttering, all external dependencies that are not installable with package managers are supposed to sit in the `dependencies` folder. Scripts are provided to install these automatically.

### Development environment setup

1- Clone the base repository on a location of your choice.

```
git clone git@github.com:DazEdword/synology-toolset.git
```

2- Configure your `.env.private` file and ssh keys as explained in the [credentials section](#credentials).


### Running tests
Docker should handle everything for you. Alternatively, a virtual environment could be created and all dependencies installed via scripts.

#### Python unit tests
Simply execute `tests.docker` script in the root, and it will install all dependencies and run the test suite.

#### Bash unit tests




