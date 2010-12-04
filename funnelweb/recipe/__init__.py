# -*- coding: utf-8 -*-
"""Recipe funnelweb"""

from zc.recipe.egg.egg import Scripts
from urllib import pathname2url as url
from sys import argv
import logging
from pkg_resources import resource_string, resource_filename


logging.basicConfig(level=logging.DEBUG)

class Recipe(Scripts):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        args = {}
        for k,v in self.options.items():
            if '-' not in k:
                continue
            part,key = k.split('-',1)
            args.setdefault(part, {})[key] = v
        default = buildout['buildout']['directory']+'/var/cache'
        
        self.options['scripts'] = 'funnelweb=%s'%name


        self.options['eggs'] = """
                transmogrify.webcrawler
                transmogrify.siteanalyser
                transmogrify.htmlcontentextractor
                transmogrify.pathsorter
                transmogrify.ploneremote
                funnelweb
                """ + self.options.get('eggs','')
        self.options['arguments'] =  str(args)
        return  Scripts.__init__(self, buildout, name, options)

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here




        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return Scripts.install(self)

    def update(self):
        """Updater"""
        return Scripts.update(self)
