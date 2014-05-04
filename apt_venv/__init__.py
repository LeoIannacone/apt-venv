import os
from xdg import BaseDirectory
from shutil import rmtree
from apt_venv import utils
from subprocess import call

class AptVenv(object):
    def __init__(self, release):
        self.release = release
        self.name = 'apt-venv'
        self.debian = ['stable', 'testing', 'unstable', 'experimental']
        self.ubuntu = ['lucid', 'precise', 'saucy', 'trusty', 'utopic']
        self.distro = None
        if self.release in self.debian:
            self.distro = 'debian'
        elif self.release in self.ubuntu:
            self.distro = 'ubuntu'
        if not self.distro:
            raise ValueError('Distro %s not valid. Please specify one of:\n' + \
                "Debian: %s\n" % ', '.join(self.debian) + \
                "Ubuntu: %s" % ', '.join(self.ubuntu))
        self.config_path = BaseDirectory.save_config_path(self.name)
        self.cache_path = BaseDirectory.save_cache_path(self.name)
        self.data_path = BaseDirectory.save_data_path(self.name)
        self.config_path = "%s/%s" % (self.config_path, self.release)
        self.cache_path = "%s/%s" % (self.cache_path, self.release)
        self.data_path = "%s/%s" % (self.data_path, self.release)
        
        self.bashrc = "%s/%s" % (self.config_path, "bash.rc")
        self.sourceslist = "%s/%s" % (self.config_path, "sources.list")
        self.aptconf = "%s/%s" % (self.config_path, "apt.conf")

    def check(self):
        pass

    def create(self):
        self.create_base()
        self.create_apt_conf()
        self.create_sources_list()
        self.create_bashrc()

    def create_base(self):
        os.makedirs(self.config_path)
        os.makedirs(os.path.join(self.data_path, \
            "var/lib/apt/lists/partial"))
        os.makedirs(os.path.join(self.data_path, \
            "var/cache/apt/archives/partial"))
        os.makedirs(os.path.join(self.data_path, \
            "etc/apt/apt.conf.d"))
        os.makedirs(os.path.join(self.data_path, \
            "etc/apt/preferences.d"))
        os.symlink('/etc/apt/trusted.gpg', \
            os.path.join(self.data_path, 'etc/apt/trusted.gpg'))
        os.makedirs(os.path.join(self.data_path, \
            "var/lib/dpkg"))
        open(os.path.join(self.data_path, \
            "var/lib/dpkg/status"), 'a').close()

    def create_apt_conf(self):
        content = utils.get_template('apt.conf') % {'base': self.data_path}
        utils.create_file(self.aptconf, content)

    def create_sources_list(self):
        content = utils.get_template('sources.list_%s' % self.distro)
        content = content % {"distro": self.release}
        utils.create_file(self.sourceslist, content)
        link = os.path.join(self.data_path, "etc/apt/sources.list")
        if not os.path.lexists(link):
            os.symlink(self.sourceslist, link)

    def create_bashrc(self):
        args = {}
        args['aptconf'] = self.aptconf
        args['data_path'] = self.data_path
        args['release'] = self.release
        content = utils.get_template('bash.rc') % args
        utils.create_file(self.bashrc, content)

    def run(self):
        call('bash --rcfile %s' % self.bashrc, shell=True)

    def delete(self):
        for directory in [self.config_path, \
            self.cache_path, self.data_path]:
            if os.path.isdir(directory):
                rmtree(directory)
