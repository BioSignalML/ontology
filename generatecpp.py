import sys, os, time
import biosignalml.rdf as rdf


ONTOLOGY = 'http://www.biosignalml.org/ontologies/2011/04/biosignalml'
SOURCE   = '2011-04-biosignalml.ttl'

PREFIXES = { 'owl':  'http://www.w3.org/2002/07/owl#',
             'dcterms': 'http://purl.org/dc/terms/',
             'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
             'bsml':  '%s#' % ONTOLOGY,
           }

CLASSES = [ 'owl:Class', 'owl:ObjectProperty', 'owl:DatatypeProperty', 'owl:NamedIndividual' ]


def abbreviate(u):
#-----------------
  s = str(u) if u else ''
  for p, n in PREFIXES.items():
    if s.startswith(n): return ''.join([p, ':', s[len(n):]])
  return s


if __name__ == '__main__':
#-------------------------

  fullname = 'file://' + os.path.abspath(SOURCE)

  g = rdf.Graph.create_from_resource(fullname, rdf.Format.TURTLE)
  VERSION = None
  for r in g.query('\n'.join(['prefix %s: <%s>' % (p, u) for p, u in PREFIXES.items()]
                           + ['',
                              'select ?version where {',
                              '  <%s> a owl:Ontology ; owl:versionInfo ?version .' % ONTOLOGY,
                              '  }'])):
    VERSION = r['version']
    break
  if VERSION is None:
    sys.exit("'%s' does not contain '%s' ontology" % (SOURCE, ONTOLOGY))

  header = [
    '/**',
    'Provide access to the BioSignalML ontology.',
    '',
    'Generated from %s at %s' % (fullname, time.strftime('%H:%H:%S %a %d %b %Y')),
    '',
    'Full documentation of the ontology is at %s.html' % ONTOLOGY,
    '**/',
    '',
    '#ifndef BSML_ONTOLOGY_H',
    '#define BSML_ONTOLOGY_H',
    '',
    '#include "rdf/rdf.h"',
    '#include "rdf/defs.h"',
    '',
    'namespace bsml {',
    '',
    '  class BSML {',
    '   public:',
    '    static const rdf::Namespace NS ;',
    ]

  implementation = [
    '#include "bsml.h"',
    '',
    'namespace bsml {',
    '  const rdf::Namespace BSML::NS("bsml", "%s#") ;' % ONTOLOGY,
    '',
    ]

  lastcls = ''
  for r in g.query('\n'.join(['prefix %s: <%s>' % (p, u) for p, u in PREFIXES.items()]
                           + ['',
                              'select distinct ?class ?subject where {',
                              '  ?subject a ?class .',
                              '  filter( ' + ' || '.join(['?class = %s' % c for c in CLASSES]) + ' )',
                              '  } order by ?class ?subject'])):
    cls  = abbreviate(r['class'])
    subj = abbreviate(r['subject'])
    if lastcls != cls:
      header.append('\n// %s resources:' % cls)
      lastcls = cls
    if subj.startswith('bsml:'):
      res = subj[5:]
      header.append('    static const rdf::URI %s ;' % res)
      implementation.append('  const rdf::URI BSML::%s = BSML::NS.make_URI("%s") ;' % (res, res))

  header.extend([
    '    } ;',
    '',
    '  } ;',
    '',
    '#endif',
    ])
  with open('ontology.h', 'w') as f:
    f.write('\n'.join(header))

  implementation.append('  } ;')
  with open('ontology.cpp', 'w') as f:
    f.write('\n'.join(implementation))

