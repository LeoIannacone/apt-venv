#!/usr/bin/python3
from distutils.core import setup
from apt_venv import VERSION

setup(name='apt_venv',
      version=VERSION,
      author='Leo Iannacone',
      author_email='l3on@ubuntu.com',
      description='virtual environment for apt',
      url='https://github.com/LeoIannacone/apt-venv',
      license='GNU GPL-3',
      scripts=['apt-venv'],
      packages=['apt_venv'],
      requires=['pyxdg'],
      data_files=[
          ('share/man/man1', ['man/apt-venv.1']),
          ('share/doc/apt-venv', ['README.md', 'AUTHORS']),
          ('/etc', ['etc/apt-venv.conf']),
          ('/usr/share/bash-completion/completions',
           ['share/bash-completion/completions/apt-venv'])
      ],
      )
