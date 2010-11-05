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

You can also crawl a local directory of html with relative links ::

 $> bin/funnelweb --crawler:site_url=file://mydirectory
 
or if the local directory contains html saved from a website and might have absolute urls in it ::

 $> bin/funnelweb --crawler:site_url=http://therealsite.com --crawler:cache=mydirectory
 



Templates
---------

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

 $> bin/funnelweb Ðpipeline > pipeline.cfg
 $> {edit} pipeline.cfg
 $> bin/funnelweb --pipeline=pipeline.cfg

See transmogrifier documentation to see how to add your own blueprints or add blueprints that
already exist to your custom pipeline.





