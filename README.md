#apt virtual environment

Quickly collect information about packages in different Debian and Ubuntu release.

**apt-venv** creates a sort of virtual environments in `$HOME/.local/share/apt-venv`, one for each release, where **apt** thinks to be on another distro/release. In these sessions a `$APT_VENV` variable is set and points out the release name in use.

If you want to customize environment you can modify files in:
```
ls $HOME/.config/apt-venv/$release
```
**apt-venv** is already available in Debian.

## Use case
To show which version of some package is in Debian and Ubuntu, simply:
```
# init apt database for releases
for release in unstable stable trusty lucid ; do
    apt-venv $release -u
done

# do what you want
for release in unstable stable trusty lucid ; do
    apt-venv $release -c "apt-cache madison base-files | grep Source | tail -1"
done
```
If you do not specify **-c** option you will entry an interactive shell.

##Usage
```
$ apt-venv -h
usage: apt-venv [-h] [-D DEBUG] [-v] [-d] [-c COMMAND] [-l] [release]

positional arguments:
  release               the debian/ubuntu release

optional arguments:
  -h, --help            show this help message and exit
  -D DEBUG, --debug DEBUG
                        set debug level
  -v, --version         show program's version number and exit
  -c COMMAND, --command COMMAND
                        exec the given command instead of entry the interactive shell
  -d, --delete          delete venv for release
  -l, --list            list all venv installed in your system
  -u, --update          update the apt indexes
```
