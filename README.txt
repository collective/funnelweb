.. contents::

FunnelWeb
=========

Easily import sites into Plone.

The simplest way to install is via a buildout recipe

  [funnelweb]
  recipe = funnelweb
  crawler-site_url=http://www.whitehouse.gov

This is will create a script to import content from the whitehouse.gov. The script will

1. Crawl
2. Cache locally
3. Filters
4. Removes template (automatically or via rules)
5. Restructures
6. Determines title,hidden from navigation etc 
7. Uploads to plone, or saves to directory

e.g.

$> bin/funnelweb --crawler:site_url=http://www.whitehouse.gov --crawler:max=50 --localupload:output=var/funnelwebdebug --ploneupload=http://admin:admin@localhost:8080/Plone

will restrict the crawler to the first 50 pages and then convert the content into the
local directory var/funnelwebdeb and also upload into a local plone site.

Funnelweb uses a transmogrifier pipeline to perform the needed transformations and all
commandline and recipe options refer to options in the pipeline. You can view the pipeline used

$> bin/funnelweb --pipeline

You can also save this pipeline and customise it for your own needs

$> bin/funnelweb Ðpipeline > pipeline.cfg

$> {edit} pipeline.cfg

$> bin/funnelweb --pipeline=pipeline.cfg

See transmogrifier documentation to see how to add your own blueprints or use some standard blueprints


Funnelweb Blueprints
--------------------

crawler - transmogrify.webcrawler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Crawls site or cache for content

see http://pypi.python.org/pypi/transmogrify.webcrawler


cache - transmogrify.webcrawler.cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Saves content to disk


typeguess - transmogrify.webcrawler.typerecognitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sets Plone content type based on mime-type

see http://pypi.python.org/pypi/transmogrify.webcrawler#TypeRecognitor


template[1-4] - transmogrify.htmlcontentextractor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provide XPath for title, description, text etc.

http://pypi.python.org/pypi/transmogrify.htmlcontentextractor


templateauto - transmogrify.htmlcontentextractor.auto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Guesses XPaths from content

see http://pypi.python.org/pypi/transmogrify.htmlcontentextractor@auto


drop - collective.transmogrifier.sections.condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Useful to drop certain content

see http://pypi.python.org/pypi/collective.transmogrifier/#condition-section



indexguess  - transmogrify.siteanalyser.defaultpage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Move index pages into folders

Determines an item is a default page for a container if it has many links
to items in that container. 

see http://pypi.python.org/pypi/transmogrify.siteanalyser#defaultpage


titleguess - transmogrify.siteanalyser.title
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Guess page titles

see http://pypi.python.org/pypi/transmogrify.siteanalyser#title


relinker - transmogrify.siteanalyser.relinker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Moves, renames, url tidying

see http://pypi.python.org/pypi/transmogrify.siteanalyser#relinker


attachmentguess - transmogrify.siteanalyser.attach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Move attachments closer to pages

see http://pypi.python.org/pypi/transmogrify.siteanalyser#makeattachments


ploneupload - transmogrify.ploneremote.remoteconstructor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Adds content to plone via xmlrpc

see http://pypi.python.org/pypi/transmogrify.ploneremote#remoteconstructor


ploneupdate - transmogrify.ploneremote.remoteschemaupdater
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates content of existing object

see http://pypi.python.org/pypi/transmogrify.ploneremote#remoteschemaupdater

plonehide - transmogrify.ploneremote.remotenavigationexcluder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hides content not in orginal sites navigation

see http://pypi.python.org/pypi/transmogrify.ploneremote#remotenavigationexcluder


plonepublish - transmogrify.ploneremote.remoteworkflowupdater
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Publish content

see http://pypi.python.org/pypi/transmogrify.ploneremote#remoteworkflowupdater


plonealias - transmogrify.ploneremote.remoteredirector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates aliases for items that have moved

see http://pypi.python.org/pypi/transmogrify.ploneremote#remoteworkflowupdater




- Code repository: http://github.com/djay/funnelweb
- Questions and comments to http://github.com/djay/funnelweb/issues
- Report bugs at http://github.com/djay/funnelweb/issues

