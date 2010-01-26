#!/usr/bin/env python

from distutils.core import setup

setup(name='pyNFC',
      version='0.1',
      description='Pure python binding of libnfc',
      author='Gabriele Modena',
      author_email='gm@nowave.it',
      url='http://github.com/gmodena/pyNFC',
      packages=['libnfc'],
      license=['BSD'],
     )

