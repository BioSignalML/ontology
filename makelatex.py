import os, time

import biosignalml.rdf as rdf


BSML_NAMESPACE = 'http://www.biosignalml.org/ontologies/2011/04/biosignalml#'

SOURCE = '2011-04-biosignalml.ttl'


PREFIXES = { 'owl':  'http://www.w3.org/2002/07/owl#',
             'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
             'dc':   'http://purl.org/dc/elements/1.1/',
             'xsd':  'http://www.w3.org/2001/XMLSchema#',
             'bsml':  BSML_NAMESPACE,
           }

PROPERTIES = [ ( [('Class', 'owl:Class')],
                 { 'label':      ('',                   'rdfs:label'),
                   'desc':       ('',                   'dc:description'),
                   'comment':    ('',                   'rdfs:comment'),
                   'seealso':    ('',                   'rdfs:seeAlso'),
                   'type':       ('',                   'a'),
                   'superclass': ('Sub class of',       'rdfs:subClassOf'),
                   'equivclass': ('Equivalent Class',   'owl:equivalentClass') },
                 { 'subclasses': ('Has sub class',      'rdfs:subClassOf'),
                   'domain':     ('Properties include', 'rdfs:domain'),
                   'range':      ('Used with',          'rdfs:range') }
               ),
               ( [('Property', 'owl:ObjectProperty'),
                  ('Property', 'owl:DatatypeProperty')],
                 { 'label':      ('',                   'rdfs:label'),
                   'desc':       ('',                   'dc:description'),
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


def abbreviate(u):
#-----------------
  s = str(u) if u else ''
  for p, n in PREFIXES.iteritems():
    if s.startswith(n): return ''.join([p, ':', s[len(n):]])
  return s



class Term(object):
#------------------

  def __init__(self, uri, kind, referto, referby):
  #-----------------------------------------------
    self.uri = uri
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
      if n != 's':
        v = abbreviate(r)
        if v:
          l = self.attributes.get(n)
          if v not in l: l.append(v)

  def latex(self):
  #---------------
    l = [ ]
    if self.attributes.get('label'):
      l.append(' '.join(self.attributes.get('label')))
    desc = '\\par'.join(self.attributes.get('desc')
                      + self.attributes.get('comment')
                      + self.attributes.get('seealso'))
    if desc: l.append(desc)
    doc = [ '\\textbf{\\large %s: %s}' % (self.kind, abbreviate(self.uri)),
            '\\par URI: \\url{%s}' % self.uri,
            '\\par %s' %  ' --- '.join(l),
          ]
    atts = [ ]
    for p in PRINTORDER:
      l = self.attributes.get(p, None)
      if l:
        l.sort()
        atts.append('\\item[%s:] %s' % (self.prompts[p], ' '.join(l)))
    l = self.attributes.get('type')
    if l:
      l.sort()
      for t in l:
        atts.append('\\item[%s]' % t)
    if atts:
      doc.append('\\begin{ontolist}')
      doc += atts
      doc.append('\\end{ontolist}')
    doc.append('\\vspace{3ex}')
    doc.append('')
    return '\n'.join(doc)


if __name__ == '__main__':
#-------------------------

  fullname = 'file://' + os.path.abspath(SOURCE)

  lastcls = ''
  g = rdf.Graph.create_from_resource(fullname, rdf.Format.TURTLE)


  term = None
  lasturi = ''
  print '{\\sffamily\\setlength{\\parindent}{0pt}'
  print('\\vspace{3ex}')
  for p in PROPERTIES:
    for k, t in p[0]:
      for r in g.query('\n'.join(['prefix %s: <%s>' % (x, u) for x, u in PREFIXES.iteritems()]
                               + ['',
                                  'select ?s ' + ' '.join(['?%s' % n for n in p[1]])
                                               + ' '.join(['?%s' % n for n in p[2]]) + ' where {'
                                  '  ?s a %s .' % t,
                                 ]
                               + ['  optional { ?s %s ?%s } .' % (r[1], n) for n, r in p[1].iteritems()]
                               + ['  optional { ?%s %s ?s } .' % (n, r[1]) for n, r in p[2].iteritems()]
                               + ['  filter regex(str(?s), "^%s")' % BSML_NAMESPACE,
                                  '  } order by ?s']
                                )):

        uri = abbreviate(r['s'])
        if uri != lasturi:
          if term: print term.latex()
          term = Term(r['s'].uri, k, p[1], p[2])
          lasturi = uri
        term.add(r)


  if term: print term.latex()
  print '}'
