SOURCES_LIST = {}

SOURCES_LIST['debian'] = """deb http://http.debian.net/debian %(distro)s main
deb-src http://http.debian.net/debian %(distro)s main

#deb http://http.debian.net/debian %(distro)s-updates main
#deb-src http://http.debian.net/debian %(distro)s-updates main

#deb http://security.debian.org/ %(distro)s/updates main
#deb-src http://security.debian.org/ %(distro)s/updates main
"""

SOURCES_LIST['ubuntu'] = \
"""deb http://archive.ubuntu.com/ubuntu/ %(distro)s main universe restricted multiverse
deb-src http://archive.ubuntu.com/ubuntu/ %(distro)s main universe restricted multiverse

deb http://security.ubuntu.com/ubuntu %(distro)s-security main universe restricted multiverse
deb-src http://security.ubuntu.com/ubuntu %(distro)s-security main universe restricted multiverse

deb http://archive.ubuntu.com/ubuntu/ %(distro)s-updates main universe restricted multiverse
deb-src http://archive.ubuntu.com/ubuntu/ %(distro)s-updates main universe restricted multiverse
"""

BASHRC = \
"""source /etc/bash.bashrc
source "${HOME}/.bashrc"
export APT_VENV="%(release)s"
export APT_CONFIG="%(aptconf)s"
export PATH="%(data_path)s/bin:${PATH}"
export PS1="(apt-venv %(release)s) ${PS1}"
"""

APT_CONF = \
"""Dir "%(data_path)s";
Dir::State::status "%(data_path)s/var/lib/dpkg/status";
"""

FAKE_SU = \
"""#!/bin/bash
echo "Sorry for this.
I must prevent you from using sudo or su in apt-venv, modifying
system and committing the biggest mistake you will ever make."
"""
