#PennToPCFG

Learns an unlexicalized PCFG from a Penn Treebank styled corpus (e.g. WallStreet Journal).

Requires NLTK2 for reading the treebank and processing the trees.

##Usage

```shell
usage: PennToPCFG.py [-h] [-p PENN] [-g GRAMMAR] [-pe PENNEVAL] [-s SENTENCES]
                     [-t TREES] [-l LENGTH] [-b DEBINARIZE DEBINARIZE]

Learns an unlexicalised PCFG from a Penn Treebank file

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
  -b DEBINARIZE DEBINARIZE, --debinarize DEBINARIZE DEBINARIZE
                        Saves the trees from the input file as unbinarized
                        trees in the output file.
```

##Examples
### Learn grammar and create evaluation data
```shell
python PennToPCFG.py --penn wsj.02-21.mrg --grammar wsjGrammar.cfg --pennEval wsj.00.mrg --sentences wsj00Sent.txt --trees wsj00Trees.txt

wsj.02-21.mrg   Contains sections 02–21 of the Wall Street Journal
wsj.00.mrg      Contains the first section if the WSJ
wsjGrammar.cfg  Will be the binarized and unlexicalized PCFG learned from the sections 02-21
wsj00Sent.txt   Will contain all the unlexicalized sentences from section 0
wsj00Trees.txt  Will contain all unbinarized and unlexicalized trees in Lisp format of section 0. 
```
---
### Debinarize trees
After parsing the sentences in *wsj00Sent.txt* with the grammar in *wsjGrammar.cfg* you need to debinarize the resulting trees before evaluating them against the gold standard trees in *wsj00Trees.txt*:

```shell
python PennToPCFG.py --debinarize ResultTrees.txt DebinarizedResultTrees.txt

ResultTrees.txt             Contains the output from your parser
DebinarizedResultTrees.txt  Will contain the debinarized trees.
```
