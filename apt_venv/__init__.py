import os
import stat
from xdg import BaseDirectory
from shutil import rmtree
from apt_venv import utils
from subprocess import call

VERSION = '0.2.0'


class AptVenv(object):
    def __init__(self, release):
        self.release = release
        self.name = 'apt-venv'
        self.debian = ['oldstable', 'stable', 'testing', 'unstable',
                       'experimental']
        self.ubuntu = ['lucid', 'precise', 'saucy', 'trusty', 'utopic']
        self.distro = None
        if self.release in self.debian:
            self.distro = 'debian'
        elif self.release in self.ubuntu:
            self.distro = 'ubuntu'
        if not self.distro:
            base = "Release \"{}\" not valid. ".format(self.release)
            if not self.release:
                base = "No release declared. "
            raise ValueError(base +
                "Please specify one of:\n" \
                " [debian] %s\n" % ' - '.join(self.debian) + \
                " [ubuntu] %s" % ' - '.join(self.ubuntu))
        self.config_path = BaseDirectory.save_config_path(self.name)
        self.cache_path = BaseDirectory.save_cache_path(self.name)
        self.data_path = BaseDirectory.save_data_path(self.name)
        self.config_path = os.path.join(self.config_path, self.release)
        self.cache_path = os.path.join(self.cache_path, self.release)
        self.data_path = os.path.join(self.data_path, self.release)

        self.bashrc = os.path.join(self.config_path, "bash.rc")
        self.sourceslist = os.path.join(self.config_path, "sources.list")
        self.aptconf = os.path.join(self.config_path, "apt.conf")

    def exists(self):
        result = True
        for myfile in [self.bashrc, self.aptconf, self.sourceslist]:
            result = result and os.path.isfile(myfile)
        utils.debug(1, "checking %s: %s" % (self.release, result))
        return result

    def create(self):
        utils.debug(1, "creating %s" % self.release)
        self.create_base()
        self.create_bin()
        self.create_apt_conf()
        self.create_sources_list()
        self.create_bashrc()

    def create_base(self):
        utils.create_dir(self.config_path)
        utils.create_dir(self.cache_path)
        utils.create_dir(os.path.join(self.data_path,\
            'var/log/apt'))
        utils.create_dir(os.path.join(self.data_path, \
            "var/lib/apt/lists/partial"))
        utils.create_dir(os.path.join(self.data_path, \
            "var/cache/apt/archives/partial"))
        utils.create_dir(os.path.join(self.data_path, \
            "etc/apt/apt.conf.d"))
        utils.create_dir(os.path.join(self.data_path, \
            "etc/apt/preferences.d"))
        utils.create_symlink('/etc/apt/trusted.gpg', \
            os.path.join(self.data_path, 'etc/apt/trusted.gpg'))
        utils.create_symlink('/etc/apt/trusted.gpg.d', \
            os.path.join(self.data_path, 'etc/apt/trusted.gpg.d'))
        utils.create_dir(os.path.join(self.data_path, \
            "var/lib/dpkg"))
        # touch dpkg status
        utils.touch_file(os.path.join(self.data_path, \
            "var/lib/dpkg/status"))

    def create_bin(self):
        bin_dir = os.path.join(self.data_path, 'bin')
        utils.create_dir(bin_dir)
        content = utils.get_template('FAKE_SU')
        bin_fakesu = os.path.join(bin_dir, '__apt-venv_fake_su')
        utils.create_file(bin_fakesu, content)
        # chmod +x bin_fakesu
        os.chmod(bin_fakesu, os.stat(bin_fakesu).st_mode | stat.S_IEXEC)
        for link in ['sudo', 'su']:
            utils.create_symlink(bin_fakesu, os.path.join(bin_dir, link))

    def create_apt_conf(self):
        content = utils.get_template('apt.conf') % {'data_path': self.data_path}
        utils.create_file(self.aptconf, content)

    def create_sources_list(self):
        content = utils.get_template('sources.list_%s' % self.distro)
        content = content % {"distro": self.release}
        utils.create_file(self.sourceslist, content)
        utils.create_symlink(
            self.sourceslist,
            os.path.join(self.data_path, "etc/apt/sources.list"))

    def create_bashrc(self):
        args = {}
        args['aptconf'] = self.aptconf
        args['data_path'] = self.data_path
        args['cache_path'] = self.cache_path
        args['release'] = self.release
        content = utils.get_template('bash.rc') % args
        utils.create_file(self.bashrc, content)

    def run(self, command=None):
        if not self.exists():
            self.create()
        bash = "bash --rcfile %s" % self.bashrc
        if command:
            bash = """bash -c "source %s ; %s" """ % (self.bashrc, command)
        utils.debug(1, "running \"%s\"" % bash)
        call(bash, shell=True)

    def update(self):
        self.run(command="apt-get update")

    def delete(self):
        utils.debug(1, "deleting %s" % self.release)
        for directory in [self.config_path,
                          self.cache_path, self.data_path]:
            if os.path.isdir(directory):
                utils.debug(2, "deleting dir %s" % directory)
                rmtree(directory)
