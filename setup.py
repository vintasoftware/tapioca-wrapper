#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re
import os
import sys

description = """
Tapioca provides an easy way to make explorable Python API wrappers.
APIs wrapped by Tapioca follow a simple interaction pattern that works uniformly so developers don't need to learn how to use a new coding interface/style for each service API.

Source code hosted on Github: https://github.com/vintasoftware/tapioca-wrapper

Documentation hosted by Readthedocs: http://tapioca-wrapper.readthedocs.io/en/stable/
"""

package = 'tapioca'
requirements = [
    'requests>=2.6',
    'arrow>=0.6.0,<1',
    'six>=1',
    'xmltodict>=0.9.2'
]
test_requirements = [
    'responses>=0.5',
    'mock>=1.3,<1.4'
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


# python setup.py register
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


setup(
    name='tapioca-wrapper',
    version=get_version(package),
    description='Python API client generator',
    long_description=description,
    author='Filipe Ximenes',
    author_email='filipeximenes@gmail.com',
    url='https://github.com/vintasoftware/tapioca-wrapper',
    packages=[
        'tapioca',
    ],
    package_dir={'tapioca': 'tapioca'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='tapioca,wrapper,api',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
