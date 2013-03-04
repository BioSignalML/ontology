REPLACE = {
  'VERSION':   "0.93.2",
  'TIMESTAMP': "2013-03-04T13:47:00+13:00",
  'DATE':      "4 March 2013",
  'CURRENT':   "20130304",
  'PREVIOUS':  "20130107",
#  'HISTORY':   """<li><p>DATE</p>
# <ul class=changes>
#  <li>change 1</li>
#  <li>change 2</li>
# </ul>
#</li>""",
  }

skel = open('template.skel', 'r')
skeleton = skel.read()
skel.close()

for key, value in REPLACE.iteritems():
  skeleton = skeleton.replace(key, value)

html = open('template.html', 'w')
html.write(skeleton)
html.close()
