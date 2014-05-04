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
    return result

def change_dir(dir):
    debug(2, "moving to directory %s" % dir)
    try:
        os.chdir(dir)
    except OSError as oserror:
        raise OSError("OSError [%d]: %s at %s" % \
          (oserror.errno, oserror.strerror, oserror.filename))

def create_file(filename, content):
    debug(2, "creating file %s" % filename)
    content = u'%s' % content
    if content[-1] != '\n':
        content += '\n'
    with codecs.open(filename, 'w', 'utf-8') as writer:
        writer.write(content)

def create_dir(dir):
    if not os.path.isdir(dir):
        debug(2, "creating directory %s" % dir)
        os.makedirs(dir)

def create_symlink(orig, dest):
    if not os.path.lexists(dest):
        debug(2, "creating symlink %s -> %s" % (orig, dest))
        os.symlink(orig, dest)
