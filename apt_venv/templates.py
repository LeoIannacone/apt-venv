BASHRC = \
"""source /etc/bash.bashrc
source "${HOME}/.bashrc"
export APT_VENV="%(release)s"
export APT_CONFIG="%(aptconf)s"
export PATH="%(data_path)s/bin:${PATH}"
export PS1="(apt-venv %(release)s) ${PS1}"
alias apt-file="apt-file -c %(cache_path)s/apt-file"
alias dd-list="dd-list -s %(data_path)s/var/lib/apt/lists/*_source_Sources"
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
