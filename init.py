#!/usr/bin/env python3
import sys
from subprocess import check_call
import os
import pip


def with_dir(dir, func):
    def wrapper(*args, **kwargs):
        cd = os.getcwd()
        os.chdir(os.path.abspath(dir))
        try:
            res = func(*args, **kwargs)
        finally:
            os.chdir(cd)
        return res
    return wrapper


def exec_django(*args):
    from django.core.management import execute_from_command_line
    return execute_from_command_line(('init.py',) + args)


def set_cwd():
    os.chdir(os.path.dirname(__file__))


def clean():
    try:
        os.remove('db.sqlite3')
    except FileNotFoundError:
        pass
    migrate()


def migrate():
    exec_django('migrate')
    exec_django('loaddata', 'courses')


def init_lang():
    exec_django('compilemessages')


def install_deps():
    check_call(('bower', 'install'))
    pip.main(('install', '-r', 'requirements.txt'))


def setup():
    install_deps()
    migrate()
    init_lang()


tasks = {
    'clean': with_dir('./src', clean),
    'init_lang': with_dir('./src', init_lang),
    'install': with_dir('./src', setup)
}


def main():
    _, command, *args = sys.argv

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course.settings")

    if command not in tasks:
        print('Unknown task \'{}\''.format(command))

    else:
        set_cwd()
        res = tasks[command](*args)
        if res is None:
            print('Successfully completed task \'{}\''.format(command))
        else:
            print('Running task \'{}\' failed with {}'.format(command, res))


if __name__ == '__main__':
    main()