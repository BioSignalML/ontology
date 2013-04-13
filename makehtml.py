REPLACE = {
  'VERSION':   "0.93.3",
  'TIMESTAMP': "2013-04-13T23:29:00+13:00",
  'DATE':      "13 April 2013",
  'CURRENT':   "20130413",
  'PREVIOUS':  "20130304",
  'HISTORY':
 """<li><p>13 April 2013</p>
     <ul class="changes">
      <li>Rename bsml:cutoffFrequency to bsml:filterFrequency.</li>
      <li>Define bsml:Segment and bsml:uncertainty.</li>
      <li>A bsml:Annotation *is not* a subclass of oa:Annotation.</li>
     </ul>
    </li>
    <li><p>4 March 2013</p>
     <ul class="changes">
      <li>A Recording is also a prv:DataItem.</li>
      <li>Define bsml:SemanticTag and bsml:ErrorTag classes, with bsml:ErrorTAG
       now an instance of a semantic tag.</li>
      <li>Use rdfs:label instead of dct:title to describe individuals.</li>
      <li>Remove bsml:Process class as this concept is for a separate ontology.</li>
      <li>Use 'dct' instead of 'dcterms' as DC Terms namespace prefix.</li>
      <li>Define bsml:cutoffFrequency as a property of a bsml:Filter.</li>
      <li>Update URIs for classes from the Ontology of Physical Biology.</li>
      <li>Remove statements about individuals that are no longer defined by the ontology.</li>
     </ul>
    </li>
    <li><p>7 January 2013</p>
     <ul class="changes">
      <li>Remove bsml:Format class as we now use mimetypes for recording file formats.</li>
      <li>Remove "bsml:Dataset" from ontology since "dctype:Dataset" expresses this concept
       and remove "bsml:source" as we can (and do) use "dcterms:source"; add "bsml:dataset".</li>
     </ul>
    </li>"""
  }

skel = open('template.skel', 'r')
skeleton = skel.read()
skel.close()

for key, value in REPLACE.iteritems():
  skeleton = skeleton.replace(key, value)

html = open('template.html', 'w')
html.write(skeleton)
html.close()
