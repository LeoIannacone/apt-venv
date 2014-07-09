from apt_venv import templates as templates
import codecs as _codecs
import os as _os

DEBUG_LEVEL = 0


def debug(level, msg):
    if level <= DEBUG_LEVEL:
        print(" debug [%s] - %s" % (level, msg))


def get_template(filename):
    result = None
    if filename == 'sources.list_ubuntu':
        result = templates.SOURCES_LIST['ubuntu']
    elif filename == 'sources.list_debian':
        result = templates.SOURCES_LIST['debian']
    elif filename == 'bash.rc':
        result = templates.BASHRC
    elif filename == 'apt.conf':
        result = templates.APT_CONF
    elif filename == 'FAKE_SU':
        return templates.FAKE_SU
    return result


def create_file(filename, content):
    if not _os.path.isfile(filename):
        debug(2, "creating file {}".format(filename))
        content = u'%s' % content
        if not content or content[-1] != '\n':
            content += '\n'
        with _codecs.open(filename, 'w', 'utf-8') as writer:
            writer.write(content)


def touch_file(filename):
    if not _os.path.isfile(filename):
        debug(2, "touching file {}".format(filename))
        open(filename, 'a').close()


def create_dir(directory):
    if not _os.path.isdir(directory):
        debug(2, "creating directory {}".format(directory))
        _os.makedirs(directory)


def create_symlink(orig, dest):
    if _os.path.exists(orig) and not _os.path.lexists(dest):
        debug(2, "creating symlink {} -> {}".format(orig, dest))
        _os.symlink(orig, dest)
