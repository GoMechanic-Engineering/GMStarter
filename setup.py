from setuptools import setup
import io
import os
import re

# long_description = ('The Firebase Admin Python SDK enables server-side (backend) Python developers '
#                     'to integrate Firebase into their services and applications.')

def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

def read_md(f):
    return io.open(f, 'r', encoding='utf-8').read()

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}

version = get_version('gmstarter')

install_requires = [
    'confluent-kafka'
]

setup(
    name="GMStarter",
    version=version,
    description='GMStarter Pack',
    long_description="GMStarter Pack for GoMechanic Python installations",
    url="https://github.com/GoMechanic-Engineering/GMStarter",
    author="Ashish Yadav, Prasenjit Singh",
    license="BSD-3-Clause",
    keywords='gomechanic',
    install_requires=install_requires,
    # packages=['gmstarter'],
    packages=get_packages('gmstarter'),
    package_data=get_package_data('gmstarter'),
    python_requires='>=3.5',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment'
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)