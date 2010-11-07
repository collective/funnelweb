FunnelWeb - Content conversion made easy
========================================

Easily convert content from existing sites into Plone.

- Code repository: http://github.com/djay/funnelweb
- Questions and comments to http://github.com/djay/funnelweb/issues
- Report bugs at http://github.com/djay/funnelweb/issues

.. contents::

Introduction
------------

Funnelweb is very easy to get started with via a few settings in either buildout
or the commandline. The predefined options have been
well thought out and have proved useful on many site convertions over the years.
Funnelweb is also very powerful since if the included transformations aren't
enough for your needs, funnelweb is built on a modular
transformation archtecture called transmogrifier. This allows you to insert
transformation steps from yourself or others to fit any site conversion need.


The simplest way to install is via a buildout recipe ::

  [funnelweb]
  recipe = funnelweb
  crawler-url=http://www.whitehouse.gov
  ploneupload-target=http://admin:admin@localhost:8080/Plone

The above example will create a script to import content from the whitehouse.gov and upload
it to a local plone site via xmlrpc. This can be run by ::

 $> bin/funnelweb

The script will

1. Crawl
2. Cache locally so subsequent crawls are quicker
3. Filters
4. Removes template (automatically or via rules)
5. Restructures
6. Determines title,hidden from navigation etc 
7. Uploads to plone, or saves html to local directory


History
-------

- 2008 Built to import large corporate intranet
- 2009 released pretaweb.funnelweb (deprecated). Built into Plone UI > Actions > Import
- 2010 Spit blueprints into transmogrify.* release on pypi
- 2010 collective.developermanual sphinx to plone uses funnelweb blueprints
- 2010 funnelweb Recipe + Script released



Options
-------

Funnelweb uses a transmogrifier pipeline to perform the needed transformations and all
commandline and recipe options refer to options in the pipeline. All the options below
can either be given as options to the buildout recipe or can be overridden via the commandline.
For instance ::

  [funnelweb]
  recipe = funnelweb
  crawler-url=http://www.whitehouse.gov

::

 $> bin/funnelweb 

and ::

 $> bin/funnelweb --crawler:url=http://www.whitehouse.gov

will do the same thing.


Crawling
~~~~~~~~

For example ::

 $> bin/funnelweb --crawler:url=http://www.whitehouse.gov --crawler:max=50 --localupload:output=var/funnelwebdebug --ploneupload=http://admin:admin@localhost:8080/Plone

will restrict the crawler to the first 50 pages and then convert the content into the
local directory var/funnelwebdeb and also upload into a local plone site.

You can also crawl a local directory of html with relative links ::

 $> bin/funnelweb --crawler:url=file:///mydirectory
 
or if the local directory contains html saved from a website and might have absolute urls in it ::

 $> bin/funnelweb --crawler:url=http://therealsite.com --crawler:cache=mydirectory

The following will not crawl anything larget than 4Mb ::

 $> bin/funnelweb --crawler:maxsize=400000

To skip crawling links by regular expression ::
 
  [funnelweb]
  recipe = funnelweb
  crawler-url=http://www.whitehouse.gov
  crawler-ignore = \.mp3
                   \.mp4 

If funnelweb is having trouble parsing the html of some pages you can preprocesses
the html before it is parsed. e.g. ::

  [funnelweb]
  recipe = funnelweb
  crawler-patterns = (<script>)[^<]*(</script>)
  crawler-subs = \1\2
  
If you'd like to skip processing links with certain mimetypes you can use the
drop:condition. This TALES expression determines what will be processed further ::

  [funnelweb]
  recipe = funnelweb
  drop-condition: python:item.get('_mimetype') not in ['application/x-javascript','text/css','text/plain','application/x-java-byte-code'] and item.get('_path','').split('.')[-1] not in ['class']


Templates
~~~~~~~~~

Funnelweb has a built clustering algorithm that tries to automatically extract the content from the html template.
This is slow and not always effective. Often you will need to input your own template extraction rules.

Rules are in the form of ::

  (title|description|text|anything) = (text|html|optional) XPath
  
For example ::

  [funnelweb]
  recipe = funnelweb
  crawler-site_url=http://www.whitehouse.gov
  ploneupload-target=http://admin:admin@localhost:8080/Plone
  template1-title       = text //div[@class='body']//h1[1]
  template1-_delete1    = optional //div[@class='body']//a[@class='headerlink']
  template1-_delete2    = optional //div[contains(@class,'admonition-description')]
  template1-description = text //div[contains(@class,'admonition-description')]//p[@class='last']
  template1-text        = html //div[@class='body']
 
In the default pipeline there are four templates called template1, template2, template3 and template4.

If not all XPaths are matched in the previous template then the next template will be tried.

When a XPath is applied within a single template, the html it matches will be removed from the page.
Another rule in that same template can't match the same html fragment.

If content part is not useful to Plone, ie text, title or description it is a way to effectively remove that html
from the content.

For more information about XPath see
- http://www.w3schools.com/xpath/default.asp
- http://blog.browsermob.com/2009/04/test-your-selenium-xpath-easily-with-firebug/

Note that spaces in XPaths must be escaped as &#32;

Site Analysis
~~~~~~~~~~~~~

In order to provide a cleaner looking plone site there are several options analysis
the entire crawler site and clean it up. These are turned off by default.

To determine if an item is a default page for a container if it has many links
to items in that container even if not contained in that folder and then move
it to that folder use ::

 $> bin/funnelweb --indexguess:condition=python:True

You can automatically find better page titles by analysing backlink text ::

  [funnelweb]
  recipe = funnelweb
  titleguess-condition = python:True
  titleguess-ignore =
	click
	read more
	close
	Close
	http:
	file:
	img


The following will finds items only referenced by one page and moves them into
a new folder with the page as the default view. ::

 $> bin/funnelweb --attachmentguess:condition=python:True

or the following will only move attachments that are images and use index-html as the new
name for the default page of the newly created folder ::

  [funnelweb]
  recipe = funnelweb
  attachmentguess-condition = python: subitem.get('_type') in ['Image']
  attachmentguess-defaultpage = index-html

The following will tidy up the urls based on a TALES expression ::

 $> bin/funnelweb --urltidy:link_expr="python:item['_path'].endswith('.html') and item['_path'][:-5] or item['_path']"

Plone Uploading
~~~~~~~~~~~~~~~

Uploading happens via remote xmlrpc calls so can be done to a live running site anywhere.

To set where a the site will be uploaded to use ::

 $> bin/funnelweb --ploneupload:target=http://username:password@myhost.com/myfolder
 
Currently only basic authentication via setting the username and password in the url is supported. If no target
is set then the site will be crawled but not uploaded.

If you'd like to change the type of what's uploaded ::

 $> bin/funnelweb --changetype:value=python:{'Folder':'HelpCenterReferenceManualSection','Document':HelpCenterLeafPage}.get(item['_type'],item['_type'])

By default funnelweb will automatically set aliases based on the orignal crawled urls so that any old links
will automatically be redirected to the new cleaned up urls. You can disable this by ::

 $> bin/funnelweb --plonealias:target=

You can change what items get published to which state by setting the following ::

  [funnelweb]
  recipe = funnelweb
  publish-value = python:["publish"]
  publish-condition = python:item.get('_type') != 'Image' and not options.get('disabled')

Funnelweb will hide certain items from plones navigation if that item was only ever linked
to from within the content area. You can disable this behavior by ::

 $> bin/funnelweb --plonehide:target=
 
You can get a local file representation of what will be uploaded by using the following ::

 $> bin/funnelweb --localupload:output=var/mylocaldir
 

Funnelweb Pipeline
------------------

Funnelweb uses a transmogrifier pipeline to perform the needed transformations and all
commandline and recipe options refer to options in the pipeline.

see funnelweb/runner/pipeline.cfg
or type ::
 $> bin/funnelweb --pipeline


.. include:: funnelweb/runner/pipeline.cfg
   :literal:


Customising the pipeline
------------------------

You can view pipeline and all it's options via the following command ::

 $> bin/funnelweb --pipeline

You can also save this pipeline and customise it for your own needs ::

 $> bin/funnelweb –pipeline > pipeline.cfg
 $> {edit} pipeline.cfg
 $> bin/funnelweb --pipeline=pipeline.cfg

Customising the pipeline allows you add your own personal transformations which
haven't been pre-considered by the standard funnelweb tool.

See transmogrifier documentation to see how to add your own blueprints or add blueprints that
already exist to your custom pipeline.





