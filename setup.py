#!/usr/bin/env python3.6
import sys
from pathlib import Path
from setuptools import setup, find_packages

if not sys.version_info >= (3, 6):
    raise RuntimeError('lzo_indexer requires at least python 3.6')

readme = Path('README.rst').read_text()

requirements = Path('requirements.txt').read_text().splitlines()
test_requirements = Path('requirements_dev.txt').read_text().splitlines()

setup(
    author='Tom Arnfeld',
    author_email='tom@duedil.com',
    maintainer='Andriy Kushnir (Orhideous)',
    maintainer_email='me@orhideous.name',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Library for indexing LZO compressed files',
    install_requires=requirements,
    license="Apache Software License",
    long_description=readme,
    include_package_data=True,
    keywords=['lzo', 'archive', 'indexing'],
    name='python3_lzo_indexer',
    packages=find_packages(),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Orhideous/python3_lzo_indexer',
    version='0.2.2',
    zip_safe=False,
    entry_points='''
        [console_scripts]
        lzo_indexer=lzo_indexer.cli:cli
    ''',
)
