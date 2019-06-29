# Synology Toolset

A Python API wrapper and toolset for interfacing with Synology NAS devices using DiskStation Manager (DSM). The repository provides two different toolsets to communicate with your NAS:

* API: Through a Python wrapper simplifying DSM queries.
* Command system: Through sh scripts hosted in the device, but called from any unix system capable of running `fabric`.

API requires valid credentials as described in the section below. Additionally, SSH access is required to run commands, optionally with the installation of SSH key-based authentication allowing the user to authenticate and operate with their NAS without constantly using a password.

## Setup

### Credentials

Valid credentials are expected to be stored locally, allowing the tools to connect to the device via local network. Create a new `.env.private` file by copying `.env.sample`, and add your own credentials as required:

1. IP: E.g. 192.168.1.35
2. Port: 5000 for http, and 5001 for https
3. Username: Same username you normally use to log in through the web interface
4. Password: Corresponding password

Finding out your local IP will depend on your OS, router configuration and other factors. Please refer to [DSM's User Guide](https://global.download.synology.com/download/Document/UserGuide/DSM/6.2/Syno_UsersGuide_NAServer_enu.pdf) for more details on how to get or set your device's IP. It is strongly recommended to set a static IP to your NAS, so that the commands and SSH access works reliably without the need to update IP.

*Note: Fore security reasons remember not share your personal credentials file or password! Do not commit to repository, or share it with anybody. That file should be private and stored safely, locally.*

### SSH key

`synotools` uses `fabric` (built in top of `paramiko`) to handle SSH connections. Certain assumptions are made regarding credentials configurations and SSH keys. It is recommended to set up a SSH Key in your default SO's SSH location. This [guide](https://help.github.com/en/enterprise/2.16/user/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), although focused on GitHub, can assist. Make sure to store the private key in your default location (`~/.ssh` for Unix systems), and make a note of your public key contents or location, as it will be required for the next step.

### Enabling NAS SSH access

By default terminal access is disabled in your device. Enable it as described [in the official support](https://www.synology.com/en-global/knowledgebase/SRM/help/SRM/RouterApp/admin_services#t1_1).

Then, the public key needs to be added to authorized_keys in your device, and correct permissions set. This handy [guide](https://blog.aaronlenoir.com/2018/05/06/ssh-into-synology-nas-with-ssh-key/) may help.

### Installing Deluge in your NAS

The download command uses Deluge remotely, so it has to be installed and configured before attempting.

1- Download and install [Synocomunity](https://synocommunity.com/).
2- Deluge's auth config has to include a user, password and permission level that will be used to connect remotely.
3- Deluge server's host ip and port. Defaulted to `127.0.0.1` and `58846` respectively.
4- Once those variables are set, copy them to their relevant fields in .env.private.

In order to set up Deluge, you can either:

a) Use Deluge's default username: `deluge` and password `deluge`, or
b) Create your own user, as [described here](https://dev.deluge-torrent.org/wiki/UserGuide/ThinClient).

_Note: If a user is going to be created, folders in the NAS are likely to differ compared with the guide above depending on your system. Auth file might be located in `/var/packages/deluge/target/var`, for instance._


## Using the tools

Most commands currently included in the tools are sh scripts expected to be hosted in the NAS, with either sh or python scripts that are run locally. Although most scripts can be run directly from python, a number of .docker scripts have been added so that anything can be run in one command.

### NAS script installation

This step is necessary before attempting to run any other script, as they rely in the scripts having been installed first!

```
./install.docker <your-ssh-name>

# eg ./install.docker paulo
```

Zips all scripts in `synotools/scripts`, zips them and deploys them to your NAS `~/.scripts` folder. User is taken from the `.env.private` file. SSH is required to connect to the NAS without additional authentication.

_Note: Adding ssh key to Docker `install` image means that this image should never be shared publicly (i.e. pushed to Docker repo) for security reasons._

### Download torrent
https://torrents.linuxmint.com/torrents/linuxmint-17-cinnamon-32bit-v2.iso.torrent

```python
python synotools/command/download.py "<your-torrent>"

# e.g python synotools/commands/download.py "https://torrents.linuxmint.com/torrents/linuxmint-17-cinnamon-32bit-v2.iso.torrent"

# e.g python synotools/commands/download.py "magnet:?xt=urn:btih:336165b4134e3754fa6996d881a7e7b55a40eb68&dn=archlinux-2019.06.01-x86_64.iso&tr=udp://tracker.archlinux.org:6969&tr=http://tracker.archlinux.org:6969/announce"
```

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

3- Ensure all scripts are executable.

```
cd </path/to/project/root>
find . -type f -iname "*.sh" -exec chmod +x {} \;
find docker/scripts/ -type f -exec chmod +x {} \;
```

### Running tests

Docker should handle everything for you. Alternatively, a virtual environment could be created and all dependencies installed via scripts.

#### Python unit tests

Simply execute `tests.docker` script in the root, and it will install all dependencies and run the test suite.





