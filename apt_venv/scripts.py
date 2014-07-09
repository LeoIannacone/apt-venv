from argparse import ArgumentParser as _ArgumentParser
from xdg import BaseDirectory as _BaseDirectory
from apt_venv import VERSION as _VERSION
from apt_venv import utils as _utils
from apt_venv import AptVenv as _AptVenv
import os as _os


def main():
    parser = _ArgumentParser(prog='apt-venv')
    parser.add_argument('-D', '--debug', type=int, help='set debug level')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + _VERSION)

    parser.add_argument(
        '-c', '--command',
        help="exec the given command instead of entry the interactive shell")
    parser.add_argument(
        '-d', '--delete', action="store_true",
        default=False, help="delete venv for release")
    parser.add_argument(
        '-l', '--list', action="store_true",
        help="list all venv installed in your system")
    parser.add_argument(
        '-u', '--update', action="store_true",
        help="update the apt indexes")
    parser.add_argument(
        'release', nargs='?',
        help="the debian/ubuntu release")

    args = parser.parse_args()

    if 'APT_VENV' in _os.environ:
        print("You can't run apt-venv inside apt-venv session")
        exit(1)

    if args.debug:
        _utils.DEBUG_LEVEL = args.debug

    if args.list:
        data_path = _BaseDirectory.save_data_path('apt-venv')
        dirs = _os.listdir(data_path)
        if len(dirs) > 0:
            print("Installed apt-venv:\n %s" % "\n ".join(dirs))
            exit(0)
        else:
            print("There is no apt-venv on your system")
            exit(1)

    try:
        venv = _AptVenv(args.release)
        if args.delete:
            venv.delete()
        else:
            if not venv.exists():
                venv.create()
                print(
                    "Welcome to apt virtual environment for {} release."
                    .format(venv.release))
                print("You may want run first \"apt-get update\"")
            if args.update:
                venv.update()
            else:
                venv.run(command=args.command)

    except ValueError as exception:
        print (str(exception))
        exit(1)
