import os, time
import biosignalml.rdf as rdf


BSML_NAMESPACE = 'http://www.biosignalml.org/ontologies/2011/04/biosignalml#'

SOURCE = '2011-04-biosignalml.ttl'


PREFIXES = { 'owl':  'http://www.w3.org/2002/07/owl#',
             'dc':   'http://purl.org/dc/elements/1.1/',
             'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
             'bsml':  BSML_NAMESPACE,
           }

CLASSES = [ 'owl:Class', 'owl:ObjectProperty', 'owl:DatatypeProperty', 'owl:NamedIndividual' ]


def abbreviate(u):
#-----------------
  s = str(u) if u else ''
  for p, n in PREFIXES.iteritems():
    if s.startswith(n): return ''.join([p, ':', s[len(n):]])
  return s


if __name__ == '__main__':

  fullname = 'file://' + os.path.abspath(SOURCE)

  print '\n'.join([
    '"""',
    'Provide access to the BioSignalML ontology.',
    '',
    'Generated from %s at %s' % (fullname, time.asctime()),
    '',
    'Full documentation of the ontology is at %s' % BSML_NAMESPACE[:-1],
    '"""',
    '',
    'from biosignalml.rdf import Uri, Resource, NS as Namespace',
    '',
    'class BSML(object):',
    '  uri = Uri("%s")' % BSML_NAMESPACE,
    '  NS = Namespace("%s")' % BSML_NAMESPACE,
    ])

  lastcls = ''
  g = rdf.Graph.create_from_resource(fullname, rdf.Format.TURTLE)
  for r in g.query('\n'.join(['prefix %s: <%s>' % (p, u) for p, u in PREFIXES.iteritems()]
                           + ['',
                              'select ?class ?subject ?desc ?comment where {',
                              '  ?subject a ?class .',
                              '  optional { ?subject dc:description ?desc } .',
                              '  optional { ?subject rdfs:comment ?comment } .',
                              '  filter( ' + ' || '.join(['?class = %s' % c for c in CLASSES]) + ' )',
                              '  } order by ?class ?subject'])):
    cls  = abbreviate(r['class'])
    subj = abbreviate(r['subject'])
    doc = [ ]
    if r['desc']: doc.append(str(r['desc']))
    if r['comment']: doc.append(str(r['comment']))
    docs  = '\n\n'.join(doc)
## rdfs:label

    if lastcls != cls:
      print '\n# %s resources:' % cls
      lastcls = cls

    if subj.startswith('bsml:'):
      res = subj[5:]
      print ''.join(['  ', '%-14s = ' % res, 'Resource(NS.%-15s' % (res + ')'),
                     "\n    '''%s'''" % docs if docs else ''])
