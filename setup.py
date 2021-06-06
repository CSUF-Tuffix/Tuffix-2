from setuptools import setup
import os
import sys

PKG_NAME = "Tuffix"

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, PKG_NAME, 'version.py')) as f:
    exec(f.read(), version)

setup(
    name = PKG_NAME,
    version=version['__version__'],
    description=('Tuffix Python Library'),
    long_description=long_description,
    author='Kevin Wortman, Michael Shafae, Jared Dyreson',
    author_email='jareddyreson@csu.fullerton.edu',
    url='https://github.com/JaredDyreson/Tuffix-Lib',
    license='GNU GPL-3.0',
    packages=[PKG_NAME],
    install_requires = [
      'Crypto',
      'packaging',
      'psutil',
      'pycryptodome',
      'pyfakefs',
      # 'python-apt @ git+https://salsa.debian.org/apt-team/python-apt', # appears to have a bug with DistUtil
      'python-gnupg', # unknown if we still need this
      'requests',
      'requests',
      'termcolor',
    ],
    include_package_data=True,
    classifiers=['Programming Language :: Python :: 3.8']
)
