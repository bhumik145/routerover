from setuptools import setup, find_packages
import sys, os

VERSION = '0.3'

setup(name='eventful',
      version=VERSION,
      author="Chris Radcliff",
      author_email='api-developers@eventful.com',
      url='http://api.eventful.com/libs/python/',
      download_url='http://api.eventful.com/libs/python/dist/eventful-%s.tar.gz' % VERSION,
      description='A client for the Eventful API.',
      license='MIT',
      long_description="""
A client for Eventful's API (http://api.eventful.com/).

Uses httplib2 and simplejson.
      """,
      install_requires=[
          'simplejson',
          'httplib2',
      ],
      py_modules=['eventful'],
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
        ])
