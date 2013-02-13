# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
setup(name='GraphGit',
      description='Git repository graph generator',
      author='Ashish Prasad (codemaniac)',
      author_email='ashish.ap.rao@gmail.com',
      url = "https://github.com/codemaniac/graphgit",
      version='0.1.1',
      packages=['graphgit'],
      scripts=['bin/graphgit'],
      install_requires=['argparse', 'networkx', 'GitPython'],
      license = "BSD",
      keywords = "git repository graph visualization network analytics"
      )
