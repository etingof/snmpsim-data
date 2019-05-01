#
# Copyright (c) 2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/snmpsim/license.html
#
"""SNMP simulation data

This package includes a collection of SNMP dumps from different
real-world SNMP-managed devices and software.
"""
import glob
import os
import sys

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Information Technology
Intended Audience :: System Administrators
Intended Audience :: Telecommunications Industry
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 2.4
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Communications
Topic :: System :: Monitoring
Topic :: System :: Networking :: Monitoring
"""


def howto_install_setuptools():
    print("""
   Error: You need setuptools Python package!

   It's very easy to install it, just type:

   wget https://bootstrap.pypa.io/ez_setup.py
   python ez_setup.py

   Then you could make eggs from this package.
""")


try:
    from setuptools import setup

    params = {
        'zip_safe': False  # this is due to data dirs
    }

except ImportError:
    for arg in sys.argv:
        if 'egg' in arg:
            howto_install_setuptools()
            sys.exit(1)

    from distutils.core import setup

    params = {}

doclines = [x.strip() for x in (__doc__ or '').split('\n') if x]

params.update(
    {'name': 'snmpsim-data',
     'version': open(os.path.join('snmpsim_data', '__init__.py')).read().split('\'')[1],
     'description': doclines[0],
     'long_description': ' '.join(doclines[1:]),
     'maintainer': 'Ilya Etingof <etingof@gmail.com>',
     'author': 'Ilya Etingof',
     'author_email': 'etingof@gmail.com',
     'url': 'https://github.com/etingof/snmpsim-data',
     'license': 'BSD',
     'platforms': ['any'],
     'classifiers': [x for x in classifiers.split('\n') if x],
     'packages': ['snmpsim_data']}
)

# install .snmprec files as data_files
for x in os.walk('data'):
    files = []
    files.extend(glob.glob(os.path.join(x[0], '*.snmprec')))

    if 'data_files' not in params:
        params['data_files'] = []

    params['data_files'].append(
        (os.path.join('snmpsim_data', *os.path.split(x[0])), files))

setup(**params)
