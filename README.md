#apt virtual environment

Fast collect information about packages in different Debian and Ubuntu release.

**apt-venv** creates a sort of virtual environments in `$HOME/.local/share/apt-venv`, one for each release, and forces apt to run under some custom option.

For more information and customization, you want take a look at these files:
```
ls $HOME/.config/apt-venv/$release
```

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
##Example
To know which version of some package is in Debian and Ubuntu:
```
# init apt database
for release in unstable stable trusty lucid ; do
    apt-venv $release -u
done

# do what you want
for release in unstable stable trusty lucid ; do
    apt-venv $release -c "apt-cache madison base-files | grep Source"
done
``` 

If you do not specify **-c** option you will entry an interactive shell.
