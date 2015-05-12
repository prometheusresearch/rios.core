#
# Copyright (c) 2015, Prometheus Research, LLC
#


from setuptools import setup, find_packages


setup(
    name='prismh.core',
    version='0.1.0',
    description='Parsing and Validation library for PRISMH Files',
    long_description=open('README.rst', 'r').read(),
    keywords='prismh instrument assessment validation',
    author='Prometheus Research, LLC',
    author_email='contact@prometheusresearch.com',
    license='AGPLv3',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    url='https://bitbucket.org/prometheus/prismh.core',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=True,
    include_package_data=True,
    namespace_packages=['prismh'],
    install_requires=[
        'six>=1.8,<2',
        'colander>=1.0,<1.1',
        'pyyaml',
    ],
    extras_require={
        'dev': [
            'coverage>=3.7,<4',
            'nose>=1.3,<2',
            'nosy>=1.1,<2',
            'prospector[with_pyroma]>=0.10,<0.11',
            'twine>=1.5,<2',
            'wheel>=0.24,<0.25',
            'Sphinx>=1.3,<2',
            'sphinx-autobuild>=0.5,<0.6',
        ],
    },
    test_suite='nose.collector',
)

