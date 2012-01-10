#!/bin/sh
rapper -i turtle -o rdfxml 2011-04-biosignalml.ttl > biosignalml.rdf
../specgenv6 --prefix=bsml --ns=http://www.biosignalml.org/ontologies/2011/04/biosignalml# \
             --indir=. --ontofile=biosignalml.rdf                                          \
             --outfile=biosignalml.html
