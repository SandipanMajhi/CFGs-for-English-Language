# CFG for English Language

This program designs context free grammars for english. The grammars include adjectives, verbs, pronouns, clauses, questions and tenses.

The randsent.py allows the following options :

  --grammar, -g
  Path to grammar file
  --start_symbol, -s
  Start symbol of the grammar (default is ROOT)
  --num_sentences, -n
  Number of sentences to generate (default is 1)
  --max_expansions, -M
  Max number of nonterminals to expand when generating a sentence
  --tree, -t
  Print the derivation tree for each generated sentence

If you want to test a grammar file, put -g followed by the grammar file name. Now, given a parse of a sentence, it can be piped into the prettyprint program to get the hierarchical version of the parse tree. 

use parse program to parse a user supplied sentence in prettyprint format -

  python3 randsent.py -g grammar.gr -n 5 | ./parse -g grammar.gr | ./prettyprint



