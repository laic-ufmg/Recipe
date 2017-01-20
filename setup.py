#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sys import platform
from setuptools import setup
from setuptools.command.install import install
from distutils.command.build import build
from subprocess import call

def calculate_version():
    initpy = open('recipe/_version.py').read().split('\n')
    version = list(filter(lambda x: '__version__' in x, initpy))[0].split('\'')[1]
    return version

package_version = calculate_version()

class RecipeBuild(build):
    def run(self):
        # run original build code
        build.run(self)

        cmd = 'make'

        def compile():
            call(cmd)

        self.execute(compile, [], 'Compiling Recipe')


class RecipeClean(build):
    def run(self):
        # run original build code
        build.run(self)

        cmd = 'make clean'
      
        def compile():
            call(cmd, shell=True)

        self.execute(compile, [], 'Cleaning Recipe')

setup(
    name='RECIPE',
    version=package_version,
    author='Walter José and Alex de Sá',
    author_email='walterjgsp@dcc.ufmg.br or alexgcsa@dcc.ufmg.br',
    url='https://github.com/RecipeML/Recipe',
    license='GNU/GPLv3',
    description=('Resilient Classification Pipeline Evolution'),
    long_description="read('README.md')",
    install_requires=['numpy', 'scipy', 'scikit-learn', 'update_checker', 'tqdm'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],

    keywords=['pipeline optimization', 'data science', 'machine learning', 'genetic programming', 'evolutionary computation'],

    cmdclass={
        'build': RecipeBuild,
        'install': RecipeBuild,
        'clean': RecipeClean,
	}    
)