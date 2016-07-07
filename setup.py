"""
Flask-Swagger-UI
-------------------

Flask Swagger.ui integration
"""
import os
import re
from setuptools import setup


def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version(os.path.join("flask_swagger_ui", "__init__.py"))

setup(
    name='Flask-Swagger-UI',
    version=__version__,
    url='http://github.com/yoophi/flask-swagger-ui/',
    license='MIT License',
    author='Pyunghyuk Yoo',
    author_email='yoophi@gmail.com',
    description='Swagger-ui integration for Flask project',
    long_description=__doc__,
    packages=['flask_swagger_ui'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'PyYAML==3.11',
        'Flask-Swagger==0.2.12',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
