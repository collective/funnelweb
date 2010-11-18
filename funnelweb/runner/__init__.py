from collective.transmogrifier.tests import registerConfig
from collective.transmogrifier.transmogrifier import Transmogrifier
from pkg_resources import resource_string, resource_filename
from collective.transmogrifier.transmogrifier import configuration_registry
import funnelweb
try:
    from Zope2.App import zcml
except:
    from Products.Five import zcml
import sys

class Context:
    pass


 
def runner(args={}):

    for k,_,v in [a.partition('=') for a in sys.argv[1:]]:
        k = k.lstrip('--')
        if ':' in k:
            part,_,key = k.partition(':')
            args.setdefault(part, {})[key] = v
        else:
            args[k] = v

    config = resource_filename(__name__,'pipeline.cfg')
    if args.get('pipeline') == '':
        f = open(config)
        print f.read()
        f.close()
        return
    else:
        config = args.get('pipeline', config)

    zcml.load_config('configure.zcml', funnelweb)


    context = Context()
    configuration_registry.registerConfiguration(
        u'transmogrify.config.funnelweb',
        u"",
        u'', config)

    transmogrifier = Transmogrifier(context)
    overrides = {}
    if type(args) == type(''):
      for arg in args:
        section,keyvalue = arg.split(':',1)
        key,value = keyvalue.split('=',1)
        overrides.setdefault('section',{})[key] = value
    else:
        overrides = args
        
    transmogrifier(u'transmogrify.config.funnelweb', **overrides)


