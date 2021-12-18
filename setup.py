import os.path
import shutil
import sys
from setuptools import setup, find_packages, Command
import os
from pathlib import Path
import atexit
from javabuilder import JavaBuilder
import argparse


def flush_temp():
    shutil.rmtree('PyCASCLib/jdk', ignore_errors=True)
    jdk_path = Path('PyCASCLib', 'jdk_path.txt')
    jcasc_path = Path('PyCASCLib', 'JCASC.jar')
    if jdk_path.exists():
        jdk_path.unlink()
        print('Deleted jdk_path.txt')
    if jcasc_path.exists():
        jcasc_path.unlink()
        print('Deleted JCASC.jar')


arg_parser = argparse.ArgumentParser(description='PyCASCLib setup')
arg_parser.add_argument('--new', dest='fresh_install_args', action='store', nargs='*', type=str, help='''
Allows you to install PyCASCLib from scratch by downloading jdk and jcasc. If --version is not specified, version 16 
will be used eg. python setup.py install --new --version=16''')
arg_parser.add_argument('--version=VALUE', dest='version', action='store', nargs=1, type=int)
arg_parser.add_argument('--jdkpath VALUE', dest='jdk_install_args', action='store', nargs=1, type=str, help='''Allow 
you to specify the path to the jdk eg. python setup.py install 
--jdkpath=C:\\Program Files\\Java\\jdk-11.0.2_11''')
args, unknown = arg_parser.parse_known_args()
fresh_install_args = args.fresh_install_args
version = args.version
jdk_install_args = args.jdk_install_args
builder = JavaBuilder()

if fresh_install_args is not None:
    if version is not None:
        builder.load(None, version[0])
    else:
        builder.load(None, 16)
    atexit.register(flush_temp)
elif jdk_install_args is not None:
    builder.load(jdk_install_args[0])
    atexit.register(flush_temp)
sys.argv = sys.argv[:2]

setup(
    name='PyCasclib',
    packages=find_packages(),
    include_package_data=True,
    version='1.0.0',
    description="Tiny wrapper for DSG's JCASCLib",
    long_description='This allows you to use JCASCLib with the help of cli and extract files, read from memory.\n' +
                     'Methods are: read_temp, open_image, read_text, read_file \n',

    author='Rigborn',
    author_email='rigborn4@gmail.com',
    py_modules=['PyCASCLib'],
    python_requires='>=3.6',
)
