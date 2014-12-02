#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Johannes Gontrum <gontrum@uni-potsdam.de>'

# Learns an unlexicalized PCFG from a Penn Treebank - like corpus (e.g. WallStreet Journal),
# Features:
#     * Has the ability to create a file containing the sentences from the given treebank file.
#     * Can also create a file containing the trees from the treebank - one tree per line.
#     * The sets of terminal symbols and non-terminal symbols in the grammar will be distinct.
#       If a tree has a 'rule' 'NNP -> NNP' where the 'NNP' on the rhs is a terminal symbol in the
#       unlexicalized grammar, it will be replaced by the rule '_NNP_ -> NNP'.

###### Imports #########################################################################
import argparse
from nltk.corpus import BracketParseCorpusReader
import nltk
import sys
from os import path

###### Variables #########################################################################
start_symbol = ""  #< The startsymbol of the grammar as string.

terminals = set()  #< The set of all found terminal symbols (String)
nonterminals = set()  #< A Set of nonterminals (NLTK.Nonterminal)
pos = set()  #< Set of all POS-tags. A POS tag is a direct parent of a leaf in the tree.
symbolMap = dict()  #< Maps ambigous nonterminals to a unique replacement

alteredTrees = list()
productions = dict()
ntCounter = dict()
grammar = list()

rhs_set = set()

sentences = list()

###### Functions #########################################################################

## Sets up the command line options
def createArgParser ():
    parser = argparse.ArgumentParser(description='Learns an unlexicalised PCFG from a Penn Treebank file')
    parser.add_argument("-p", "--penn", help="The Penn Treebank file.", required=True)
    parser.add_argument("-g", "--grammar", help="File to write the PCFG to.", required=True,
                        type=argparse.FileType('w'))
    parser.add_argument("-pe", "--pennEval",
                        help="The Penn Treebank file that is used to read the sentences and the trees from. If not specified it uses the file to create the grammar from.",
                        required=False)
    parser.add_argument("-s", "--sentences", help="File to write the sentences to.", required=False,
                        type=argparse.FileType('w'))
    parser.add_argument("-t", "--trees", help="File to write the trees to.", required=False,
                        type=argparse.FileType('w'))
    parser.add_argument("-l", "--length", help="Maximum length of the sentences for the evaluation (default=30)",
                        required=False,
                        type=int, default=30)

    return parser


## Split symbols in terminals and nonterminals
def findSymbolsInTree (tree):
    # Basecase: Still a tree
    if type(tree) == nltk.Tree:
        nonterminals.add(tree.node)
        if len(tree) == 1 and tree.height() == 2:
            pos.add(tree.node)  # found a POS tag
        for subtree in tree:
            findSymbolsInTree(subtree)  # Go on recursively
    # Recursive case: It's a String
    else:
        terminals.add(tree)


## Replace ambiguous symbols
def replaceSymbolsInTree (tree, sent):
    if tree.node in symbolMap:
        tree.node = symbolMap[tree.node]
    # iterate over all subtrees...
    for i in range(len(tree)):
        # Case: The subtree is a leaf (String)
        if type(tree[i]) != nltk.Tree:
            tree[i] = revertPOS(tree.node)
            sent.append(tree[i])
            pass
        # Recursive case
        else:
            replaceSymbolsInTree(tree[i], sent)

## Turns a _A_ symbol back to A
def revertPOS(symbol):
    return symbol[1:-1]

###### Main #########################################################################
if __name__ == '__main__':
    clArgs = createArgParser().parse_args()

    ## Set up the treebank reader
    ptb = BracketParseCorpusReader(path.dirname(clArgs.penn), [path.basename(clArgs.penn)])

    ## Collect all terminal and nonterminals
    for tree in ptb.parsed_sents(ptb.fileids()[0]):
        # Also set the start symbol to the root of the first tree
        if len(start_symbol) == 0:
            start_symbol = tree.node
        findSymbolsInTree(tree)


    ## Find ambiguous symbols and map them to a unique alternative
    for symbol in nonterminals.intersection(pos):
        replacement = "_" + symbol + "_"
        symbolMap[symbol] = replacement
        if replacement in pos or replacement in nonterminals:
            print "Cannot make nonterminal unambiguous: ", symbol
            sys.exit(-1)

    ## Iterate over all trees and replace ambigous nonterminals with their unique alternative
    for tree in ptb.parsed_sents(ptb.fileids()[0]):
        newTree = tree.copy(True)

        # Remove unary rules and convert to CNF
        newTree.chomsky_normal_form(horzMarkov=2)
        newTree.collapse_unary(collapsePOS=False)

        replaceSymbolsInTree(newTree, [])

        # newTree.draw()

        ## Count production occupancies
        for production in newTree.productions():
            if len(production.rhs()) == 0:
                production = nltk.grammar.Production(production.lhs(), [revertPOS(production.lhs())])

            # Update the symbol and rule counter
            if production.lhs() in ntCounter:
                ntCounter[production.lhs()] += 1
            else:
                ntCounter[production.lhs()] = 1

            if production in productions:
                productions[production] += 1
            else:
                productions[production] = 1

    # Check if the start symbol must be replaced
    if start_symbol in symbolMap:
        start_symbol = symbolMap[start_symbol]

    ## Time to write the PCFG
    clArgs.grammar.write(start_symbol + "\n")
    for prod in productions:
        rhs_set.add(prod.rhs())
        ret = "{0} -> ".format(prod.lhs())
        for sym in prod.rhs():
            ret += ("{0} ".format(sym))
        ret += ("[" + str(productions[prod] / float(ntCounter[prod.lhs()])) + "]")
        clArgs.grammar.write(ret + "\n")

    ## Check if we have to handle the optional arguments
    evalSentences = False
    evalTrees = False

    if clArgs.sentences != None:
        evalSentences = True

    if clArgs.trees != None:
        evalTrees = True

    ## Go on creating evaluation data
    if evalSentences or evalTrees:
        evalFile = clArgs.penn
        if clArgs.pennEval:
            evalFile = clArgs.pennEval

        ptb_eval = BracketParseCorpusReader(path.dirname(evalFile), [path.basename(evalFile)])

        for tree in ptb_eval.parsed_sents(ptb_eval.fileids()[0]):
            newTree = tree.copy(True)
            # Transform the trees for evaluation in exactly the same way as done for the grammar
            newTree.chomsky_normal_form(horzMarkov=2)
            newTree.collapse_unary(collapsePOS=False)

            sent = []
            replaceSymbolsInTree(newTree, sent)
            if len(sent) <= clArgs.length:
                if evalSentences:
                    clArgs.sentences.write(" ".join(sent) + "\n")
                if evalTrees:
                    clArgs.trees.write(newTree._pprint_flat('', "()", False) + "\n")
