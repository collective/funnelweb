from collective.transmogrifier.tests import registerConfig
from collective.transmogrifier.transmogrifier import Transmogrifier
from pkg_resources import resource_string, resource_filename
from collective.transmogrifier.transmogrifier import configuration_registry
import funnelweb
from optparse import OptionParser, OptionGroup

import sys
import ConfigParser

import logging
try:
    from Zope2.App import zcml
except:
    from Products.Five import zcml

logging.basicConfig(level=logging.INFO)
                    

class Context:
    pass


class NoErrorParser(OptionParser):
    def error(self):
        pass
 
def runner(args={}):
    parser = OptionParser()
    
    parser.add_option("-p", "--pipeline", dest="pipeline",
                  help="Transmogrifier pipeline.cfg to use", metavar="FILE")
    
    pargs = [arg for arg in sys.argv[1:] if arg in ['--pipeline','-p']]
    (options, cargs) = parser.parse_args(pargs)
    if options.pipeline is None:
        config = resource_filename(__name__,'pipeline.cfg')
    else:
        config = options.get('pipeline')
    cparser = ConfigParser.RawConfigParser()
    cparser.read(config)
    pipeline = [p.strip() for p in cparser.get('transmogrifier','pipeline').split()]
    for section in pipeline:
        if section == 'transmogrifier':
            continue
        if cparser.has_option(section,'@doc'):
            doc = cparser.get(section,'@doc')
        else:
            doc = ''
        group = OptionGroup(parser, section, doc)
        for key,value in cparser.items(section):
            if key.startswith('@'):
                if key == '@doc':
                    continue
                metavar,_,help = value.partition(': ')
                if metavar.upper() == metavar:
                    action = "store"
                else:
                    action = "store_true"
                    help = value
                group.add_option("--%s:%s"%(section,key[1:]), action=action,
                                             help=help,
                                             metavar=metavar)
        parser.add_option_group(group)
    pargs = [arg for arg in sys.argv[1:] if not arg.startswith('--template') ]
    (options, cargs) = parser.parse_args(pargs)

    
    cargs = {}
    for k,_,v in [a.partition('=') for a in sys.argv[1:]]:
        k = k.lstrip('--')
        if ':' in k:
            part,_,key = k.partition(':')
            if key.lower()=='debug':
                logger = logging.getLogger(part)
                logger.setLevel(logging.DEBUG)
            else:
                section = cargs.setdefault(part, {})
                if key in section:
                    section[key] = '%s\n%s' % (section[key],v)
                else:
                    section[key] = v
        else:
            cargs[k] = v
            
    args.update(cargs)

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


