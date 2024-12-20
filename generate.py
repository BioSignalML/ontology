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
  for p, n in PREFIXES.iteritems():
    if s.startswith(n): return ''.join([p, ':', s[len(n):]])
  return s


if __name__ == '__main__':
#-------------------------

  fullname = 'file://' + os.path.abspath(SOURCE)

  g = rdf.Graph.create_from_resource(fullname, rdf.Format.TURTLE)
  VERSION = None
  for r in g.query('\n'.join(['prefix %s: <%s>' % (p, u) for p, u in PREFIXES.iteritems()]
                           + ['',
                              'select ?version where {',
                              '  <%s> a owl:Ontology ; owl:versionInfo ?version .' % ONTOLOGY,
                              '  }'])):
    VERSION = r['version']
    break
  if VERSION is None:
    sys.exit("'%s' does not contain '%s' ontology" % (SOURCE, ONTOLOGY))

  print('\n'.join([
    '"""',
    'Provide access to the BioSignalML ontology.',
    '',
    'Generated from %s at %s' % (fullname, time.strftime('%H:%H:%S %a %d %b %Y')),
    '',
    'Full documentation of the ontology is at %s' % ONTOLOGY,
    '"""',
    '',
    'from biosignalml.rdf import Resource, NS as Namespace',
    '',
    '__all__ = [ "VERSION", "BSML" ]',
    '',
    '',
    'VERSION = "%s"' % VERSION,
    '',
    'class BSML(object):',
    '  """',
    '  RDF resources for each item in the BioSignalML ontology.',
    '  """',
    '  URI = "%s#"' % ONTOLOGY,
    '  NS = Namespace(URI)',
    '  prefix = NS.prefix',
    ]))     #'

  lastcls = ''
  for r in g.query('\n'.join(['prefix %s: <%s>' % (p, u) for p, u in PREFIXES.iteritems()]
                           + ['',
                              'select distinct ?class ?subject ?label ?desc ?comment where {',
                              '  ?subject a ?class .',
                              '  optional { ?subject rdfs:label ?label } .',
                              '  optional { ?subject dcterms:description ?desc } .',
                              '  optional { ?subject rdfs:comment ?comment } .',
                              '  filter( ' + ' || '.join(['?class = %s' % c for c in CLASSES]) + ' )',
                              '  } order by ?class ?subject'])):
    cls  = abbreviate(r['class'])
    subj = abbreviate(r['subject'])
    doc = [ ]
    if r['label']: doc.append(str(r['label']))
    if r['desc']: doc.append(str(r['desc']))
    if r['comment']: doc.append(str(r['comment']))
    docs  = '\n\n'.join(doc)

    if lastcls != cls:
      print('\n# %s resources:' % cls)
      lastcls = cls

    if subj.startswith('bsml:'):
      res = subj[5:]
      print(''.join(['  ', '%-14s = ' % res, ('Resource(NS.%-15s' % (res + ')')).rstrip(),
                     '\n  """**%s**: %s"""' % (cls, docs if docs else '')]).rstrip())
