import os
import io
import re
import codecs
from setuptools import setup, find_packages
from setuptools.command.install import install

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

# List all of your Python package dependencies in the
# requirements.txt file

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\n")
        return stream.read()


readme = readfile("README.rst", split=True)[3:]  # skip title
# For requirements not hosted on PyPi place listings
# into the 'requirements.txt' file.
requires = ['PySide6',
            'numpy',
            'git+https://github.com/scardine/image_size',
            'cmlibs.utils>=0.1.4',
            'cmlibs.widgets']  # minimal requirements listing
source_license = readfile("LICENSE")


class InstallCommand(install):

    def run(self):
        install.run(self)
        # Automatically install requirements from requirements.txt
        import subprocess
        subprocess.call(['pip', 'install', '-r', os.path.join(SETUP_DIR, 'requirements.txt')])


setup(
    name='mapclientplugins.imagebasedfiducialmarkersstep',
    version=find_version("mapclientplugins", "imagebasedfiducialmarkersstep", "__init__.py"),
    description='',
    long_description='\n'.join(readme) + source_license,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    cmdclass={'install': InstallCommand,},
    author='Hugh Sorby',
    author_email='',
    url='',
    license='APACHE',
    packages=find_packages(exclude=['ez_setup', ]),
    namespace_packages=['mapclientplugins'],
    include_package_data=True,
    zip_safe=False,
    requires=requires,
)
