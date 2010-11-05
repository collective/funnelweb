FunnelWeb
=========

Easily import sites into Plone.

- Code repository: http://github.com/djay/funnelweb
- Questions and comments to http://github.com/djay/funnelweb/issues
- Report bugs at http://github.com/djay/funnelweb/issues

.. contents::

Introduction
------------

The simplest way to install is via a buildout recipe ::

  [funnelweb]
  recipe = funnelweb
  crawler-site_url=http://www.whitehouse.gov
  ploneupload-target=http://admin:admin@localhost:8080/Plone

This is will create a script to import content from the whitehouse.gov. This can be run by ::

 $> bin/funnelweb

The script will

1. Crawl
2. Cache locally so subsequent crawls are quicker
3. Filters
4. Removes template (automatically or via rules)
5. Restructures
6. Determines title,hidden from navigation etc 
7. Uploads to plone, or saves html to local directory

e.g. ::

  $> bin/funnelweb --crawler:site_url=http://www.whitehouse.gov --crawler:max=50 --localupload:output=var/funnelwebdebug --ploneupload=http://admin:admin@localhost:8080/Plone

will restrict the crawler to the first 50 pages and then convert the content into the
local directory var/funnelwebdeb and also upload into a local plone site.

Funnelweb uses a transmogrifier pipeline to perform the needed transformations and all
commandline and recipe options refer to options in the pipeline. You can view the pipeline used

.. include:: funnelweb/runner/pipeline.cfg
   :literal:


Customising the pipeline
------------------------

You can view pipeline and all it's options via the following command ::

 $> bin/funnelweb --pipeline

You can also save this pipeline and customise it for your own needs ::

 $> bin/funnelweb Ðpipeline > pipeline.cfg
 $> {edit} pipeline.cfg
 $> bin/funnelweb --pipeline=pipeline.cfg

See transmogrifier documentation to see how to add your own blueprints or add blueprints that
already exist to your custom pipeline.





