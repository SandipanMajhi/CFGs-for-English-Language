#!/usr/bin/env python3
"""
Adapted from Jason Eisner's NLP course
"""
import os
import sys
import random
import argparse

# Want to know what command-line arguments a program allows?
# Commonly you can ask by passing it the --help option, like this:
#     python randsent.py --help
# This is possible for any program that processes its command-line
# arguments using the argparse module, as we do below.
#
# NOTE: When you use the Python argparse module, parse_args() is the
# traditional name for the function that you create to analyze the
# command line.  Parsing the command line is different from parsing a
# natural-language sentence.  It's easier.  But in both cases,
# "parsing" a string means identifying the elements of the string and
# the roles they play.

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        args (an argparse.Namespace): Stores command-line attributes
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description="Generate random sentences from a PCFG")
    # Grammar file (required argument)
    parser.add_argument(
        "-g",
        "--grammar",
        type=str, required=True,
        help="Path to grammar file",
    )
    # Start symbol of the grammar
    parser.add_argument(
        "-s",
        "--start_symbol",
        type=str,
        help="Start symbol of the grammar (default is ROOT)",
        default="ROOT",
    )
    # Number of sentences
    parser.add_argument(
        "-n",
        "--num_sentences",
        type=int,
        help="Number of sentences to generate (default is 1)",
        default=1,
    )
    # Max number of nonterminals to expand when generating a sentence
    parser.add_argument(
        "-M",
        "--max_expansions",
        type=int,
        help="Max number of nonterminals to expand when generating a sentence",
        default=450,
    )
    # Print the derivation tree for each generated sentence
    parser.add_argument(
        "-t",
        "--tree",
        action="store_true",
        help="Print the derivation tree for each generated sentence",
        default=False,
    )
    return parser.parse_args()


class Grammar:
    def __init__(self, grammar_file):
        """
        Context-Free Grammar (CFG) Sentence Generator

        Args:
            grammar_file (str): Path to a .gr grammar file
        
        Returns:
            self
        """
        # Parse the input grammar file
        self.rules = {}
        self._load_rules_from_file(grammar_file)

    def _load_rules_from_file(self, grammar_file):
        """
        Read grammar file and store its rules in self.rules

        Args:
            grammar_file (str): Path to the raw grammar file 
        """

        with open(grammar_file, 'r') as f:
            for line in f:
                if(line[0] not in ['#',' ','\n']):
                    if(line.find('#') != -1):
                        line = line[:line.find('#')]
                    if "\t" in line:
                        line_splits = line.strip().split("\t")
                    else:
                        line_splits = line.strip().split(" ")
                    # print(line_splits)
                    if line_splits[1] not in self.rules:
                        self.rules[line_splits[1]] = [[],[]]
                        self.rules[line_splits[1]][0].append(line_splits[2])
                        self.rules[line_splits[1]][1].append(float(line_splits[0]))
                    else:
                        self.rules[line_splits[1]][0].append(line_splits[2])
                        self.rules[line_splits[1]][1].append(float(line_splits[0]))

        for key, value in self.rules.items():
            value[1][:] = [x/ sum(value[1]) for x in value[1]]

        # print(self.rules)

        # raise NotImplementedError

    def sample(self, derivation_tree, max_expansions, start_symbol):
        """
        Sample a random sentence from this grammar

        Args:
            derivation_tree (bool): if true, the returned string will represent 
                the tree (using bracket notation) that records how the sentence 
                was derived
                               
            max_expansions (int): max number of nonterminal expansions we allow

            start_symbol (str): start symbol to generate from

        Returns:
            str: the random sentence or its derivation tree
        """
        
        #### Non Tree Version

        if derivation_tree: 
            tree_sentence = ""
            production = random.choices(population = self.rules[start_symbol][0], 
                                        weights = self.rules[start_symbol][1])

            if start_symbol == "ROOT":
                self.root_expansion_limit = max_expansions - 1
                tree_sentence += "(" + start_symbol + " "
            else:
                tree_sentence += start_symbol + " "

            self.root_expansion_limit = self.root_expansion_limit - 1

            for query in production[0].split():
                if self.root_expansion_limit > 0:
                    if query in self.rules:
                        tree_sentence += "(" + self.sample(derivation_tree, max_expansions, query) + ")"
                    else:
                        tree_sentence += query + " "

            if start_symbol == "ROOT":
                tree_sentence += ")"
            
            return tree_sentence
            
        else :

            random_sentence = ""
            production = random.choices(population = self.rules[start_symbol][0], 
                                        weights = self.rules[start_symbol][1])

            if start_symbol == "ROOT":
                self.root_expansion_limit = max_expansions - 1

            self.root_expansion_limit = self.root_expansion_limit - 1

            for query in production[0].split():
                if self.root_expansion_limit > 0:
                    if query in self.rules:
                        random_sentence += self.sample(derivation_tree,max_expansions,query) + ' '
                    else:
                        random_sentence +=  query + ' '
            
            return random_sentence.strip()


####################
### Main Program
####################
def main():
    # Parse command-line options
    args = parse_args()

    # Initialize Grammar object
    grammar = Grammar(args.grammar)

    # Generate sentences
    for i in range(args.num_sentences):
        # Use Grammar object to generate sentence
        sentence = grammar.sample(
            derivation_tree=args.tree,
            max_expansions=args.max_expansions,
            start_symbol=args.start_symbol
        )

        # Print the sentence with the specified format.
        # If it's a tree, we'll pipe the output through the prettyprint script.
        if args.tree:
            prettyprint_path = os.path.join(os.getcwd(), 'prettyprint')
            t = os.system(f"echo '{sentence}' | perl {prettyprint_path}")
        else:
            print(sentence)


if __name__ == "__main__":
    main()
