# -*- coding: utf-8 -*-
"""
This module contains the tool of funnelweb
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.1'

long_description = (
    read('README.rst')
    + '\n' +
    'Contributors\n' 
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' + 
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )


tests_require=['zope.testing', 'zc.buildout']

setup(name='funnelweb',
      version=version,
      description="Crawl and parse static sites and import to Plone",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout crawler spider plone',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='http://pypi.python.org/pypi/funnelweb',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        'collective.transmogrifier',
                        'transmogrify.webcrawler>=1.1',
                        'transmogrify.siteanalyser>=1.2',
                        'transmogrify.htmlcontentextractor>=1.0',
                        'transmogrify.ploneremote>=1.2',
                        'Products.CMFCore',
                        'zope.app.pagetemplate',
                        'zope.app.component',
                        'mr.migrator>=1.0b11',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'funnelweb.recipe.tests.test_docs.test_suite',
      entry_points = {"zc.buildout": ["default = funnelweb.recipe:Recipe"],
                      'console_scripts': ['funnelweb = funnelweb.runner:runner'],
                      "z3c.autoinclude.plugin":['target = plone'],
                      "z3c.autoinclude.plugin":['target = transmogrify'],
                      },
      )
