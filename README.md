#PennToPCFG

Learns an unlexicalized PCFG from a Penn Treebank - like corpus (e.g. WallStreet Journal).

Requires NLTK.

##Usage:

```
usage: PennToPCFG.py [-h] -p PENN -g GRAMMAR [-pe PENNEVAL] [-s SENTENCES]
                     [-t TREES] [-l LENGTH]

Learns an unlexicalized PCFG from a Penn Treebank file

optional arguments:
  -h, --help            show this help message and exit
  -p PENN, --penn PENN  The Penn Treebank file.
  -g GRAMMAR, --grammar GRAMMAR
                        File to write the PCFG to.
  -pe PENNEVAL, --pennEval PENNEVAL
                        The Penn Treebank file that is used to read the
                        sentences and the trees from. If not specified it uses
                        the file to create the grammar from.
  -s SENTENCES, --sentences SENTENCES
                        File to write the sentences to.
  -t TREES, --trees TREES
                        File to write the trees to.
  -l LENGTH, --length LENGTH
                        Maximum length of the sentences for the evaluation
                        (default=30)
```
