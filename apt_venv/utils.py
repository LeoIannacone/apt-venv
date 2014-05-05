from apt_venv import templates
import codecs
import os

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
    if not os.path.isfile(filename):
        debug(2, "creating file %s" % filename)
        content = u'%s' % content
        if not content or content[-1] != '\n':
            content += '\n'
        with codecs.open(filename, 'w', 'utf-8') as writer:
            writer.write(content)

def touch_file(filename):
    if not os.path.isfile(filename):
        debug(2, "touching file %s" % filename)
        open(filename, 'a').close()

def create_dir(directory):
    if not os.path.isdir(directory):
        debug(2, "creating directory %s" % directory)
        os.makedirs(directory)

def create_symlink(orig, dest):
    if os.path.exists(orig) and not os.path.lexists(dest):
        debug(2, "creating symlink %s -> %s" % (orig, dest))
        os.symlink(orig, dest)
