cp 2011-04-biosignalml.ttl website/biosignalml-$1.ttl
cp biosignalml.rdf website/biosignalml-$1.rdf
cp biosignalml.html website/biosignalml-$1.html

cd website
rm biosignalml.ttl
rm biosignalml.rdf
rm biosignalml.html
ln -s biosignalml-$1.ttl  biosignalml.ttl
ln -s biosignalml-$1.rdf  biosignalml.rdf
ln -s biosignalml-$1.html biosignalml.html
git add biosignalml-$1.ttl  biosignalml.ttl
git add biosignalml-$1.rdf  biosignalml.rdf
git add biosignalml-$1.html biosignalml.html
