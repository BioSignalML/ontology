Update Python classes in core library:::

  python generate.py > ontology.py
  mv ontology.py ~/biosignalml/corelib/biosignalml/model/


Generate LaTeX documentation:::

  python makelatex.py  > ontology.tex


Releasing a new Web version:

* Ensure all changes are committed.
* Run `gitlog.sh` to get change history.
* Update version, timestamp, dates, and history information in `makehtml.py`.
* Commit changed `makehtml.py` and `git tag` the release.
* Then:::

    # RELEASE is value of CURRENT in makehtml.py
    python makehtml.py
    git commit makehtml.py
    git tag -m"RELEASE" RELEASE
    ./makedoc.sh
    ./installdoc RELEASE
    cd website
    git commit .
    git tag -m"RELEASE" RELEASE
    git push

