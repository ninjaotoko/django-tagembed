# -*- coding:utf8 -*-
#
# Copyright (c) 2014 Xavier Lesa <xavierlesa@gmail.com>.
# All rights reserved.
# Distributed under the BSD license, see LICENSE
from setuptools import setup, find_packages
import sys, os
from tagembed import version

setup(name='django-tagembed', 
        version=version, 
        description="App para parsear string con custom tags y transformarlos en embeds",
        packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
        include_package_data=True,
        zip_safe=False,
        author='Xavier Lesa',
        author_email='xavierlesa@gmail.com',
        url='http://github.com/ninjaotoko/django-tagembed'
        )
