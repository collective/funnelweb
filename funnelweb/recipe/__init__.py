# -*- coding: utf-8 -*-
"""Recipe funnelweb"""

import z3c.recipe.scripts
from urllib import pathname2url as url
from sys import argv
import logging
from pkg_resources import resource_string, resource_filename


logging.basicConfig(level=logging.DEBUG)

class Recipe(z3c.recipe.scripts.scripts.Scripts):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.options.setdefault('cache-output',"%s/var/funnelwebcache"%buildout['buildout']['directory'])
        args = {}
        for k,v in self.options.items():
            if '-' not in k:
                continue
            part,key = k.split('-',1)
            args.setdefault(part, {})[key] = v
        default = buildout['buildout']['directory']+'/var/cache'
        default = args['crawler'].get('url','')
        args.setdefault('crawler',{}).setdefault('site_url',default)
        default = args.setdefault('upload',{}).get('url','')
        args.setdefault('upload',{}).setdefault('target',default)
        #args.setdefault('schemaupdater',{}).setdefault('target',default)
        #args.setdefault('publish',{}).setdefault('target',default)
        #args.setdefault('excludefromnavigation',{}).setdefault('target',default)


        self.options['eggs'] = """transmogrify.htmltesting
                transmogrify.webcrawler
                transmogrify.siteanalyser
                transmogrify.htmlcontentextractor
                transmogrify.pathsorter
                transmogrify.ploneremote
                Products.ZSQLMethods
                Products.CMFCore
                zope.app.pagetemplate
                funnelweb
                zope.app.component"""
        self.options['arguments'] =  str(args)
#        self.options['entry-points'] = '%s=transmogrify.htmltesting.runner:runner'%name
        return  z3c.recipe.scripts.scripts.Scripts.__init__(self, buildout, name, options)

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here




        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return z3c.recipe.scripts.scripts.Scripts.install(self)

    def update(self):
        """Updater"""
        return z3c.recipe.scripts.scripts.Scripts.update(self)
