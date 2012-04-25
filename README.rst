FunnelWeb - Content conversion made easy
****************************************

Easily convert content from existing html into Plone.

:Code repository: http://github.com/collective/funnelweb
:Questions and comments to: http://github.com/collective/funnelweb/issues
:Report bugs at:
  http://github.com/collective/funnelweb/issues
  https://github.com/collective/transmogrify.webcrawler/issues
  https://github.com/collective/transmogrify.htmlcontentextractor/issues
  https://github.com/collective/transmogrify.siteanalyser/issues
  https://github.com/collective/transmogrify.ploneremote/issues

.. contents::

Introduction
------------

FunnelWeb is a webcrawler which extracts website content such as titles, descriptions,
images and content blocks from existing websites. It filters this content and uploads
it into a new website which uses the `Plone`_ CMS. It gives you many options for adjusting
how content is migrated. It is an invaluable tool when you want to migrate a site which doesn't
use a CMS or there isn't a tool can migrate content directly from the sites database.

For those familar with `collective.transmogrifier`_, funnelweb is a prebuilt pipeline that combines
blueprints from four different packages (`transmogrify.webcrawler`_, `transmogrify.htmlcontentextractor`_
`transmogrify.siteanalyser`_ and `transmogrify.ploneremote`_). Due to the flexible nature of the
`collective.transmogrifier`_ framework underneath advanced users can add further steps to their conversion
process.

The work performed by the funnelweb script can be broken down into four sections:

1. Crawling the site including caching locally so subsequent crawls are quicker and filtering out
   unwanted content (`transmogrify.webcrawler`_)
2. Remove boilerplate/templates (automatically or via rules) so just content remains (`transmogrify.htmlcontentextractor`_)
3. Analysing the site structure to improve the content quality including working out titles, default
   views, types of objects to create, what to show in navigation etc (`transmogrify.siteanalyser`_)
4. Uploading to the CMS such as Plone, or saving cleaned HTML to local directory (`transmogrify.ploneremote`_)

FunnelWeb uses the `mr.migrator`_ framework which allows it's funnelweb `collective.transmogrifier`_ pipeline to be run:

1. Within Plone itself . see `mr.migrator`_ for how to install.

2. A command line script which can be installed via zc.buildout. Content is uploaded
   into `Plone`_ via it's web services API.


Installation for commandline
----------------------------

You can install via easy_install ::

  $> easy_install funnelweb

This can be run by ::

  $> buildout

Or funnelweb can be installed via a buildout recipe (see `zc.buildout`_) ::

  [buildout]
  parts += funnelweb

  [funnelweb]
  recipe = funnelweb

  $> buildout init
  $> bin/buildout


This can be run by ::

 $> bin/funnelweb

The examples here will assume installation via buildout

.. _`zc.buildout`: http://www.buildout.org

Configuration for commandline
-----------------------------

Funnelweb is organised as a series of steps through which crawled items pass before eventually being
uploaded. Each step has one or more configuration options so you can customise import process
for your needs. Almost all imports will require some level of configurations.

Funnelweb gives three methods to configure your pipeline.

Using a local pipeline configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create your own pipeline.cfg that overrides and extends the default funnelweb
pipeline.

For example, create a file called pipeline.cfg with the following ::

    [transmogrifier]
    include = funnelweb.remote

    [crawler]
    url=http://collective-docs.readthedocs.org/en/latest/

This will override the crawler blueprint setting "url". You can run this by ::

  $> bin/funnelweb --pipeline=pipeline.cfg

You can view funnelweb.remote pipeline and all its options via the following command ::

 $> bin/funnelweb --show-pipeline

You can also save this pipeline and customise it for your own needs ::

 $> bin/funnelweb --show-pipeline > pipeline.cfg
 $> {edit} pipeline.cfg
 $> bin/funnelweb --pipeline=pipeline.cfg



Commandline arguments
~~~~~~~~~~~~~~~~~~~~~

Any arguement from the pipeline can be overridden via the command-line

e.g ::

 $> bin/funnelweb --crawler:url=http://www.whitehouse.gov

All arguments are --(step:argument)=value.
The first part of each configuration key is the step e.g. `crawler`. The second part is the particular
configuration option for that particular step. e.g. `url`. This is then followed by = and value or values.

some options require multiple lines within a buildout part. These can be overridden
via the commandline by repeating the same argument e.g. ::

  $> bin/funnelweb --crawler:ignore=\.mp3 --crawler:ignore=\.pdf


You can see a list of all the arguments via ::

 $> bin/funnelweb --help


Buildout Override
~~~~~~~~~~~~~~~~~

Any command-line override can also be "baked" into the funnelweb script. e.g. ::

  [buildout]
  parts += funnelweb

  [funnelweb]
  recipe = funnelweb
  crawler-url=http://www.whitehouse.gov
  pipeline=pipeline.cfg


Any paramater of the form ::

  [step]
  blah = blah

will become in buildout ::

  [funnelweb]
  recipe = funnelweb
  step-blah = blah

and on the command line ::

  bin/funnelweb --step:blah=blah


Recommended Usage
-----------------

Below is an outline of how you might typically use funnelweb.

1. First set up buildout to make a command line funnelweb
2. Create a pipeline.cfg including funnelweb.remote (see `Using a local pipeline configuration`_)
3. Bake pipeline file into buildout (see `Buildout Override`_)
4. Test crawl your site and store it into the cache (see `Crawling - HTML to import`_)
5. You might need to set some crawler:ignore rules
6. crawl the whole site into your cache (see `Crawling - HTML to import`_)
7. Crawl the first 10 pages using --crawler:maxsize=10
8. Use `Templates`_ in debug mode to find Title, Description and Text your pages
9. `Upload to Plone`_ to test
10. if the structure and urls are what you expect use `Site Analysis`_
11. Repeat crawling more pages


Configuration Options
---------------------

The full list of steps that can be configured along with the transmogrifier
blueprint for each

1. Crawling

:crawler: `transmogrify.webcrawler`_
:cache: `transmogrify.webcrawler.cache`_
:typeguess: `transmogrify.webcrawler.typerecognitor`_
:drop: `collective.transmogrifier.sections.condition`_

2. Templates

:template1: `transmogrify.htmlcontentextractor`_
:template2: `transmogrify.htmlcontentextractor`_
:template3: `transmogrify.htmlcontentextractor`_
:template4: `transmogrify.htmlcontentextractor`_
:templateauto: `transmogrify.htmlcontentextractor.auto`_

3. Site Analysis

:sitemapper: `transmogrify.siteanalyser.sitemapper`_
:indexguess: `transmogrify.siteanalyser.defaultpage`_
:titleguess: `transmogrify.siteanalyser.title`_
:attachmentguess: `transmogrify.siteanalyser.attach`_
:hideguess: `transmogrify.siteanalyser.hidefromnav`_
:urltidy: `transmogrify.siteanalyser.urltidy`_
:addfolders: `transmogrify.pathsorter`_
:changetype: `collective.transmogrifier.sections.inserter`_

4. Uploading

:ploneupload: `transmogrify.ploneremote.remoteconstructor`_
:ploneupdate: `transmogrify.ploneremote.remoteschemaupdater`_
:plonehide: `transmogrify.ploneremote.remotenavigationexcluder`_
:publish: `collective.transmogrifier.sections.inserter`_
:plonepublish: `transmogrify.ploneremote.remoteworkflowupdater`_
:plonealias: `transmogrify.ploneremote.remoteredirector`_
:ploneprune: `transmogrify.ploneremote.remoteprune`_
:localupload: `transmogrify.webcrawler.cache`_

.. _transmogrify.webcrawler: http://pypi.python.org/pypi/transmogrify.webcrawler#transmogrify-webcrawler
.. _transmogrify.webcrawler.cache: http://pypi.python.org/pypi/transmogrify.webcrawler#transmogrify-webcrawler-cache
.. _transmogrify.webcrawler.typerecognitor: http://pypi.python.org/pypi/transmogrify.webcrawler#transmogrify-webcrawler-typerecognitor
.. _collective.transmogrifier.sections.condition: http://pypi.python.org/pypi/collective.transmogrifier#condition

.. _transmogrify.htmlcontentextractor: http://pypi.python.org/pypi/transmogrify.htmlcontentextractor#transmogrify-htmlcontentextractor
.. _transmogrify.htmlcontentextractor.auto: http://pypi.python.org/pypi/transmogrify.htmlcontentextractor#transmogrify-htmlcontentextractor.auto

.. _transmogrify.siteanalyser: http://pypi.python.org/pypi/transmogrify.siteanalyser
.. _transmogrify.siteanalyser.sitemapper: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-siteanalyser-sitemapper
.. _`transmogrify.siteanalyser.defaultpage`: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-siteanalyser-defaultpage
.. _`transmogrify.siteanalyser.title`: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-siteanalyser-title
.. _`transmogrify.siteanalyser.attach`: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-siteanalyser-attach
.. _`transmogrify.siteanalyser.hidefromnav`: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-siteanalyser-hidefromnav
.. _`transmogrify.siteanalyser.urltidy`: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-siteanalyser-urltidy
.. _`transmogrify.pathsorter`: http://pypi.python.org/pypi/transmogrify.siteanalyser#transmogrify-pathsorter
.. _collective.transmogrifier.sections.inserter: http://pypi.python.org/pypi/collective.transmogrifier#inserter

.. _`transmogrify.ploneremote`: http://pypi.python.org/pypi/transmogrify.ploneremote
.. _`transmogrify.ploneremote.remoteconstructor`: http://pypi.python.org/pypi/transmogrify.ploneremote#transmogrify-ploneremote-remoteconstructor
.. _`transmogrify.ploneremote.remoteschemaupdater`: http://pypi.python.org/pypi/transmogrify.ploneremote#transmogrify-ploneremote-remoteschemaupdater
.. _`transmogrify.ploneremote.remotenavigationexcluder`: http://pypi.python.org/pypi/transmogrify.ploneremote#transmogrify-ploneremote-remotenavigationexcluder
.. _`transmogrify.ploneremote.remoteworkflowupdater`: http://pypi.python.org/pypi/transmogrify.ploneremote#transmogrify-ploneremote-remoteworkflowupdater
.. _`transmogrify.ploneremote.remoteredirector`: http://pypi.python.org/pypi/transmogrify.ploneremote#transmogrify-ploneremote-remoteredirector
.. _`transmogrify.ploneremote.remoteprune`: http://pypi.python.org/pypi/transmogrify.ploneremote#transmogrify-ploneremote-remoteprune

or you use the commandline help to view the list of available options ::

  $> bin/funnelweb --help


The most common configuration options for these steps are detailed below.

Crawling - HTML to import
~~~~~~~~~~~~~~~~~~~~~~~~~

Funnelweb imports HTML either from a live website, from a folder on disk, or a folder
on disk with HTML which was retrieved from a live website and may still have absolute
links refering to that website.

Funnelweb can only import things it can crawl, i.e. content that is linked from
HTML. If your site contains javascript links or password protected content, then
you may have to perform some extra steps to get funnelweb to crawl your
content.

To crawl a live website, supply the crawler with a base HTTP URL to start crawling from.
This URL must be the URL which all the other URLs you want from the site start with.

For example ::

 $> bin/funnelweb --crawler:url=http://www.whitehouse.gov --crawler:maxsize=50  --ploneupload=http://admin:admin@localhost:8080/Plone

will restrict the crawler to the first 50 pages and then convert the content
into a local Plone site.

The site you crawl will be cached locally, so if you run funnelweb again it will run much quicker. If you'd like
to disable the local caching use ::

 $> bin/funnelweb --cache:output=
 
If you'd like to reset the cache, refreshing it's data, set the crawlers cache to nothing ::

 $> bin/funnelweb --crawler:cache=

By default the cache is stored in ``var/funnelwebcache/{site url}/``. You can set this to another directory using::

 $> bin/funnelweb --cache:output=my_new_dir


You can also crawl a local directory of HTML with relative links by just using a ``file://`` style URL ::

 $> bin/funnelweb --crawler:url=file:///mydirectory

or if the local directory contains HTML saved from a website and might have absolute URLs in it,
the you can set this as the cache. The crawler will always look up the cache first ::

 $> bin/funnelweb --crawler:url=http://therealsite.com --crawler:cache=mydirectory

The following will not crawl anything larger than 4Mb ::

 $> bin/funnelweb --crawler:max=400000

To skip crawling links by regular expression ::

  [funnelweb]
  recipe = funnelweb
  crawler-url=http://www.whitehouse.gov
  crawler-ignore = \.mp3
                   \.mp4 

If funnelweb is having trouble parsing the HTML of some pages, you can preprocesses
the HTML before it is parsed. e.g. ::

  [funnelweb]
  recipe = funnelweb
  crawler-patterns = (<script>)[^<]*(</script>)
  crawler-subs = \1\2

If you'd like to skip processing links with certain mimetypes you can use the
``drop:condition`` option. This TALES expression determines what will be processed further ::

  [funnelweb]
  recipe = funnelweb
  drop-condition: python:item.get('_mimetype') not in ['application/x-javascript','text/css','text/plain','application/x-java-byte-code'] and item.get('_path','').split('.')[-1] not in ['class']


Templates
~~~~~~~~~

Funnelweb has a built-in clustering algorithm that tries to automatically extract the content from the HTML template.
This is slow and not always effective. Often you will need to input your own template extraction rules.

If you'd like to turn off the automatic templates ::

 $> bin/funnelweb --templateauto:condition=python:False


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

Note that for a single template e.g. template1, ALL of the XPaths need to match otherwise
that template will be skipped and the next template tried. If you'd like to make it
so that a single XPath isn't nessary for the template to match then use the keyword `optional` or `optionaltext`
instead of `text` or `html` before the XPath.


In the default pipeline there are four templates called `template1`, `template2`, `template3` and `template4`.

When an XPath is applied within a single template, the HTML it matches will be removed from the page.
Another rule in that same template can't match the same HTML fragment.

If a content part is not useful to Plone (e.g. redundant text, title or description) it is a way to effectively remove that HTML
from the content.

To help debug your template rules you can set debug mode ::

  $> bin/funnelweb --template1:debug --template2:debug

Setting debug mode on templateauto will give you details about the rules it uses. ::

  $> bin/funnelweb --templateauto:debug
  ...
  DEBUG:templateauto:'icft.html' discovered rules by clustering on 'http://...'
  Rules:
	text= html //div[@id = "dal_content"]//div[@class = "content"]//p
	title= text //div[@id = "dal_content"]//div[@class = "content"]//h3
  Text:
	TITLE: ...
	MAIN-10: ...
	MAIN-10: ...
	MAIN-10: ...


For more information about XPath see

- http://www.w3schools.com/xpath/default.asp
- http://blog.browsermob.com/2009/04/test-your-selenium-xpath-easily-with-firebug/


Site Analysis
~~~~~~~~~~~~~

In order to provide a cleaner-looking Plone site, there are several options to analyse
the entire crawled site and clean it up. These are turned off by default.

To determine if an item is a default page for a container (it has many links
to items in that container, even if not contained in that folder), and then move
it to that folder, use ::

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
	https:
	file:
	img


The following will find items only referenced by one page and move them into
a new folder with the page as the default view. ::

 $> bin/funnelweb --attachmentguess:condition=python:True

or the following will only move attachments that are images and use ``index-html`` as the new
name for the default page of the newly created folder ::

  [funnelweb]
  recipe = funnelweb
  attachmentguess-condition = python: subitem.get('_type') in ['Image']
  attachmentguess-defaultpage = index-html

The following will tidy up the URLs based on a TALES expression ::

 $> bin/funnelweb --urltidy:link_expr="python:item['_path'].endswith('.html') and item['_path'][:-5] or item['_path']"

If you'd like to move content around before it's uploaded you can use the urltidy step as well e.g. ::

 $> bin/funnelweb --urltidy:link_expr=python:item['_path'].startswith('/news') and '/otn/news'+item['path'][5:] or item['_path']

If you want to hide content from navigation you can use `hideguess`

 $> bin/funnelweb --hideguess:condition=python:item['path']=='musthide'



Upload to Plone
~~~~~~~~~~~~~~~

Uploading happens via remote XML-RPC calls so can be done to a live running site anywhere.

To set where a the site will be uploaded to use ::

 $> bin/funnelweb --ploneupload:target=http://username:password@myhost.com/myfolder

Currently only basic authentication via setting the username and password in the url is supported. If no target
is set then the site will be crawled but not uploaded.

If you'd like to change the type of what's uploaded ::

 $> bin/funnelweb --changetype:value=python:{'Folder':'HelpCenterReferenceManualSection','Document':HelpCenterLeafPage}.get(item['_type'],item['_type'])

This will set a new value for the type of the item. You could make this conditional e.g ::

 $> bin/funnelweb --changetype:condition=python:item['_path].startswith('/news')
 
or by using a more complex expression for the new type

 $> bin/funnelweb --changetype:value=python:item['_path'].startswith('/news') and 'NewNewsType' or item['_type]


By default, funnelweb will automatically create Plone aliases based on the original crawled URLs, so that any old links
will automatically be redirected to the new cleaned-up urls. You can disable this by ::

 $> bin/funnelweb --plonealias:target=

You can change what items get published to which state by setting the following ::

  [funnelweb]
  recipe = funnelweb
  publish-value = python:["publish"]
  publish-condition = python:item.get('_type') != 'Image' and not options.get('disabled')

Funnelweb will hide certain items from Plone's navigation if that item was only ever linked
to from within the content area. You can disable this behavior by ::

 $> bin/funnelweb --plonehide:target=

You can get a local file representation of what will be uploaded by using the following ::

 $> bin/funnelweb --localupload:output=var/mylocaldir
 
Examples
--------

Feel free to fork and add your own examples for extracting content for common sites or
CMS's

Read The Docs
~~~~~~~~~~~~~

As an example the following buildout will create a funnelweb script that will
convert a regular sphinx documentation into remote Plone content
inside a PloneHelpCenter ::

    [transmogrifier]
    include = funnelweb.remote

    [crawler]
    url=http://collective-docs.readthedocs.org/en/latest/
    ignore=
            cgi-bin
            javascript:
            _static
            _sources
            genindex\.html
            search\.html
            saesrchindex\.js

    [template1]
    title = text //div[@class='body']//h1[1]
    description = optional //div[contains(@class,'admonition-description')]/p[@class='last']/text()
    text = html //div[@class='body']
    # Fields with '_' won't be uploaded to Plone so will be effectively removed
    _permalink = text //div[@class='body']//a[@class='headerlink']
    _label = optional //p[contains(@class,'admonition-title')]
    _remove_useless_links = optional //div[@id = 'indices-and-tables']

    # Images will get titles from backlink text
    [titleguess]
    condition = python:True

    # Pages linked to content will be moved together
    [indexguess]
    condition = python:True

    # Hide the images folder from navigation
    [hideguess]
    condition = python:item.get("_path","").startswith('_images') and item.get('_type')=='Folder'

    # Upload as PHC instead of Folders and Pages
    [changetype]
    value=python:{'Folder':'HelpCenterReferenceManualSection','Document':'HelpCenterLeafPage'}.get(item['_type'],item['_type'])

    # Save locally for debugging purposes
    [localupload]
    output=manual

    # All folderish content should be checked if they contain
    # any items on the remote site which are not presented locally. including base folder
    [ploneprune]
    condition=python:item.get('_type') in ['HelpCenterReferenceManualSection','HelpCenterReferenceManual'] or item['_path'] == ''

Joomla
~~~~~~

#TODO

Wordpress
~~~~~~~~~

#TODO

Drupal
~~~~~~

#TODO

Others
~~~~~~

Add your own examples here

Controlling Logging
-------------------

You can show additional debug output on any particular set by setting a debug commandline switch.
For instance to see see additional details about template matching failures ::

  $> bin/funnelweb --template1:debug
  
  

Working directly with transmogrifier (advanced)
-----------------------------------------------

You might need to insert further transformation steps for your particular
conversion usecase. To do this, you can extend funnelweb's underlying
transmogrifier pipeline. Funnelweb uses a transmogrifier pipeline to perform the needed transformations and all
commandline and recipe options refer to options in the pipeline.


You can view pipeline and all its options via the following command ::

 $> bin/funnelweb --show-pipeline

You can also save this pipeline and customise it for your own needs ::

 $> bin/funnelweb --show-pipeline > pipeline.cfg
 $> {edit} pipeline.cfg
 $> bin/funnelweb --pipeline=pipeline.cfg

Customising the pipeline allows you add your own personal transformations which
haven't been pre-considered by the standard funnelweb tool.

See transmogrifier documentation to see how to add your own blueprints or add blueprints that
already exist to your custom pipeline.

Using external blueprints
~~~~~~~~~~~~~~~~~~~~~~~~~

If you have decided you need to customise your pipeline and you want to install transformation
steps that use blueprints not already included in funnelweb or transmogrifier, you can include
them using the ``eggs`` option in a funnelweb buildout part ::

  [funnelweb]
  recipe = funnelweb
  eggs = myblueprintpackage
  pipeline = mypipeline.cfg

However, this only works if your blueprint package includes the following setuptools entrypoint
in its ``setup.py`` ::

      entry_points="""
            [z3c.autoinclude.plugin]
            target = transmogrify
            """,
            )

.. NOTE:: Some transmogrifier blueprints assume they are running inside a Plone
   process such as those in `plone.app.transmogrifier` (see http://pypi.python.org/pypi/plone.app.transmogrifier).  Funnelweb
   doesn't run inside a Plone process so these blueprints won't work. If
   you want upload content into Plone, you can instead use
   `transmogrify.ploneremote`_ which provides alternative implementations
   which will upload content remotely via XML-RPC.
   `transmogrify.ploneremote`_ is already included in funnelweb as it is
   what funnelweb's default pipeline uses.

Attributes available in funnelweb pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using the default blueprints in funnelweb the following are some of the attributes that
will become attached to the items that each blueprint has access to. These can be used in the various
condition statements etc. as well as your own blueprints.

``_site_url``
  The base of the url as passed into the webcrawler

``_path``
  The remainder of the URL. ``_site_url`` + ``_path`` = URL

``_mimetype``
  The mimetype as returned by the crawler

``_content``
  The content of the item crawled, include image, file or HTML data.

``_orig_path``
  The original path of the item that was crawled. This is useful for setting redirects so
  you don't get 404 errors after migrating content.

``_sort_order``
  An integer representing the order in which this item was crawled. Helps to determine
  what order items should be sorted in folders created on the server if your site
  has navigation which has links ordered top to bottom.

``_type``
  The type of object to be created as returned by the "typeguess" step

``title``, ``description``, ``text``, etc.
  The template steps will typically create fields with content in them taken from ``_content``

``_template``
  The template steps will leave the HTML that wasn't seperated out into different fields in this
  attribute.

``_defaultpage``
  Set on an Folder item where you want to tell the uploading steps to set the containing item
  mentioned in ``_defaultpage`` to be the default page shown on that folder instead of a content listing.

``_transitions``
  Specify the workflow action you'd like to make on an item after it's uploaded or updated.

``_origin``
  This is used internally with the `transmogrify.siteanalysis.relinker` blueprint as a way to
  tell it that you have changed the ``_path`` and you now want the relinker to find any links that
  refer to ``_origin`` to now point to ``_path``.

The Funnelweb Pipeline
~~~~~~~~~~~~~~~~~~~~~~

see http://github.com/collective/funnelweb/blob/master/funnelweb/remote.cfg
or type ::

 $> bin/funnelweb --show-pipeline


 
Contributing
------------

- Code repository: http://github.com/collective/funnelweb
- Questions and comments to http://github.com/collective/funnelweb/issues
- Report bugs at http://github.com/collective/funnelweb/issues

The code of funnelweb itself is fairly minimal. It just sets up and runs a transmogrifier pipeline.
The hard work is actually done by five packages which each contain one or more transmogrifier
blueprints. These are:

Webcrawler
  http://pypi.python.org/pypi/transmogrify.webcrawler
  https://github.com/djay/transmogrify.webcrawler

HTMLContentExtractor
  http://pypi.python.org/pypi/transmogrify.htmlcontentextractor
  https://github.com/djay/transmogrify.htmlcontentextractor
  
SiteAnalyser
  http://pypi.python.org/pypi/transmogrify.siteanalyser
  https://github.com/djay/transmogrify.siteanalyser
  
PathSorter
  http://pypi.python.org/pypi/transmogrify.pathsorter 
  https://github.com/djay/transmogrify.pathsorter  
  
PloneRemote
  http://pypi.python.org/pypi/transmogrify.ploneremote
  https://github.com/djay/transmogrify.ploneremote
  
Each has it's own issue tracker and we will accept pull requests for new functionality or bug
fixes. The current state of documentation and testing is not yet at a high level.


History
-------

- 2008 Built to import large corporate intranet
- 2009 released pretaweb.funnelweb (deprecated). Built into Plone UI > Actions > Import
- 2010 Split blueprints into transmogrify.* release on pypi
- 2010 collective.developermanual sphinx to Plone uses funnelweb blueprints
- 2010 funnelweb Recipe + Script released
- 2011 split runner out into mr.migrator




.. _`collective.transmogrifier`: http://pypi.python.org/pypi/collective.transmogrifier
.. _`Plone`: http://plone.org
.. _`mr.migrator`: http://pypi.python.org/pypi/mr.migrator

