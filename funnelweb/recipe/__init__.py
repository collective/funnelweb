# -*- coding: utf-8 -*-
"""Recipe funnelweb"""

from zc.recipe.egg.egg import Scripts
from urllib import pathname2url as url
from sys import argv
import logging
from pkg_resources import resource_string, resource_filename
from mr.migrator.recipe import Recipe as Base


logging.basicConfig(level=logging.DEBUG)

class Recipe(Base):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        args = {}
        for k,v in self.options.items():
            if '-' in k:
                part,key = k.split('-',1)
                args.setdefault(part, {})[key] = v
        default = buildout['buildout']['directory']+'/var/cache'
        
        self.options['scripts'] = 'funnelweb=%s'%name


        self.options['eggs'] = """
                mr.migrator
                transmogrify.webcrawler
                transmogrify.siteanalyser
                transmogrify.htmlcontentextractor
                transmogrify.pathsorter
                transmogrify.ploneremote
                funnelweb
                """ + self.options.get('eggs','')

        pipeline = self.options.setdefault('pipeline','funnelweb.remote')
        self.options['arguments'] =  str(args)+',"'+pipeline+'"'
        return  Base.__init__(self, buildout, name, options)

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here




        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return Base.install(self)

    def update(self):
        """Updater"""
        return Base.update(self)
