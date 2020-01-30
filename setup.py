#
# Copyright (c) 2015, Prometheus Research, LLC
#


from setuptools import setup, find_packages


setup(
    name='rios.core',
    version='0.8.4',
    description='Parsing and Validation Library for RIOS Files',
    long_description=open('README.rst', 'r').read(),
    keywords='rios prismh research instrument assessment standard validation',
    author='Prometheus Research, LLC',
    author_email='contact@prometheusresearch.com',
    license='Apache-2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://github.com/prometheusresearch/rios.core',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=True,
    include_package_data=True,
    namespace_packages=['rios'],
    entry_points={
        'console_scripts': [
            'rios-validate = rios.core.scripts:validate',
        ]
    },
    install_requires=[
        'six',
        'colander>=1.0,<1.5',
        'pyyaml',
    ],
    test_suite='nose.collector',
)

