import sys, os

import biosignalml.rdf as rdf


ONTOLOGY = 'http://www.biosignalml.org/ontologies/2011/04/biosignalml'

SOURCE   = '2011-04-biosignalml.ttl'


PREFIXES = { 'rdf':  'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
             'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
             'xsd':  'http://www.w3.org/2001/XMLSchema#',
             'owl':  'http://www.w3.org/2002/07/owl#',
             'dct':  'http://purl.org/dc/terms/',
             'time': 'http://www.w3.org/2006/time#',
             'bsml':  ONTOLOGY + '#',
           }

PROPERTIES = [ ( ( 'Class', 'Classes', ['owl:Class']),
                 { 'label':      ('',                   'rdfs:label'),
                   'desc':       ('',                   'dct:description'),
                   'comment':    ('',                   'rdfs:comment'),
                   'seealso':    ('',                   'rdfs:seeAlso'),
#                   'type':       ('',                   'a'),
                   'superclass': ('Sub class of',       'rdfs:subClassOf'),
                   'equivclass': ('Equivalent Class',   'owl:equivalentClass') },
                 { 'subclasses': ('Has sub class',      'rdfs:subClassOf'),
                   'domain':     ('Properties include', 'rdfs:domain'),
                   'range':      ('Used with',          'rdfs:range') }
               ),
               ( ( 'Property', 'Properties', ['owl:ObjectProperty', 'owl:DatatypeProperty']),
                 { 'label':      ('',                   'rdfs:label'),
                   'desc':       ('',                   'dct:description'),
                   'comment':    ('',                   'rdfs:comment'),
                   'seealso':    ('',                   'rdfs:seeAlso'),
                   'type':       ('',                   'a'),
                   'superprop':  ('Sub property of',    'rdfs:subPropertyOf'),
                   'equivprop':  ('Equivalent property', 'owl:equivalentProperty'),
                   'domain':     ('Domain',             'rdfs:domain'),
                   'range':      ('Range',              'rdfs:range') },
                 { 'subprops':   ('Has sub properties', 'rdfs:subPropertyOf') }
               ),
             ]

PRINTORDER = [ 'equivclass', 'equivprop',
               'superclass', 'superprop',
               'subclasses', 'subprops',
               'domain',     'range',
             ]


SECTION    = "section"
SELECTED   = None         # Print everything



def abbreviate(u):
#-----------------
  s = str(u) if u else ''
  for p, n in PREFIXES.iteritems():
    if s.startswith(n): return ''.join([p, ':', s[len(n):]]).replace('_', '\\_')
  return s.replace('_', '\\_').replace('#', '\\#')



class Term(object):
#------------------

  def __init__(self, uri, kind, referto, referby):
  #-----------------------------------------------
    self.uri = str(uri)
    self.kind = kind
    self.prompts = { }
    self.attributes = { }
    for n, r in referby.iteritems():
      self.prompts[n] = r[0]
      self.attributes[n] = []
    for n, r in referto.iteritems():
      self.prompts[n] = r[0]
      self.attributes[n] = []

  def add(self, results):
  #----------------------
    for n, r in results.iteritems():
      if n != 's' and r:
        v = None
        if n == 'seealso': v = str(r.uri).replace('#', '\\#')
#        elif r.is_blank() and n in ['domain', 'range']:

#          select ?c where { str(r) owl:unionOf ?c } order by ?c

        elif not r.is_blank(): v = abbreviate(r)
        if v:
          l = self.attributes.get(n)
          if v not in l: l.append(v)

  def latex(self):
  #---------------
    l = [ ]
    if self.attributes.get('label'):
      l.append(' '.join(self.attributes.get('label')))
    seealso = [ ]
    if self.attributes.get('seealso'):
##       seealso.append('See also: ' + ' '.join(self.attributes.get('seealso')))
       seealso.append('See also: ' + ' '.join(['\\url{%s}' %u for u in self.attributes.get('seealso')]))
    desc = '\n\\par '.join(self.attributes.get('desc')
                      + self.attributes.get('comment')
                      + seealso)
    if desc: l.append(desc)
##  doc = [ '\\textbf{\\large %s: %s}' % (self.kind, abbreviate(self.uri)),
    doc = [ '\\subsubsection{%s: %s}' % (self.kind, abbreviate(self.uri)),
            '\\par URI: \\url{%s}' % self.uri,
            '\\par %s' %  ' --- '.join(l),
          ]
    atts = [ ]
    for p in PRINTORDER:
      l = self.attributes.get(p, None)
      if l:
        l.sort()
        atts.append('\\item[%s:] %s' % (self.prompts[p], ', '.join(l)))
    l = self.attributes.get('type')
    if l:
      l.sort()
      for t in l:
        atts.append('\\item[%s]' % t)
    if atts:
      doc.append('\\begin{ontolist}')
      doc += atts
      doc.append('\\end{ontolist}')
##    doc.append('\\vspace{3ex}')
    doc.append('')
    return '\n'.join(doc)
    

if __name__ == '__main__':
#-------------------------

  if len(sys.argv) > 1:
    SECTION = "subsection*"
    SELECTED = [ 'bsml:Recording',
                 'bsml:Signal',
                 'bsml:Event',
                 'bsml:Annotation',
                 'bsml:Process',
                 'bsml:rate',
                 'bsml:dataBits',
                 'bsml:units',
               ]

  fullname = 'file://' + os.path.abspath(SOURCE)
  lastcls = ''
  g = rdf.Graph.create_from_resource(fullname, rdf.Format.TURTLE)
  term = None
  lasturi = ''

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

  print """The BioSignalML Ontology defines concepts used in the storage and
exchange of biosignals, along with terms for common biosignal metadata elements.
The ontology is available from \url{%(rdf)s} as RDF, with a human readable
version at \url{%(rdf)s.html}.\n""" % dict(rdf = ONTOLOGY)

  print "This documentation is generated from Version %s of the Ontology.\n" % VERSION

  print '{\\raggedright\\setstretch{1.1}\\setlength{\\parindent}{0pt}\\def\\UrlFont{\\small\\tt}'
##  print('\\vspace{3ex}')
  for p in PROPERTIES:
    if term: print term.latex()
    term = None
    print '\\%s{%s}' % (SECTION, p[0][1])
    for r in g.query('\n'.join(['prefix %s: <%s>' % (x, u) for x, u in PREFIXES.iteritems()]
                             + ['',
                                'select ?s ' + ' '.join(['?%s' % n for n in p[1]])
                                             + ' '.join(['?%s' % n for n in p[2]]) + ' where {'
                                '  ?s a ?c .',
                               ]
                             + ['  optional { ?s %s ?%s } .' % (r[1], n) for n, r in p[1].iteritems()]
                             + ['  optional { ?%s %s ?s } .' % (n, r[1]) for n, r in p[2].iteritems()]
##                             + ['  optional { ?s %s [ owl:unionOf (?u1 ?u2) ] }' % p[1][prop][1]
##                                     for prop in ['domain', 'range'] if p[1].get(prop, None) ]



                             + ['  filter( regex(str(?s), "^%s#")' % ONTOLOGY,
                                '   && ( ' + ' || '.join(['?c = %s' % c for c in p[0][2]]) + ' ) )',
                                '  } order by ?s']
                              )):

      uri = abbreviate(r['s'])
      if SELECTED is None or uri in SELECTED:
        if uri != lasturi:
          if term: print term.latex()
          term = Term(r['s'].uri, p[0][0], p[1], p[2])
          lasturi = uri
        term.add(r)

  if term: print term.latex()
  print '}'
