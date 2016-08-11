#! /usr/bin/python

# reformat_mirexpress_expression_for_easier_comparison_between_samples.py
# Aaron M. Duffy
# 2016-06-08

# The mirexpress expression output only includes miRNAs that are expressed, which makes building a master
# expression table for all samples a bit difficult. This just makes a list of expression values for ALL
# miRNAs in the same order that they are listed in the improved predicted miRNA list.
#usage: ./reformat_mirexpress_expression_for_easier_comparison_between_samples.py mirexpress_miRNA_expression.txt improved_expanded_mature_turkey_miRNAs_from_unique_hairpins-mirbase_format.txt

import sys

expression_by_mirna = {} # key = mirna name, value = expression value from mirexpress
with open(sys.argv[1]) as expression_file:
    for line in expression_file:
        elements = line.strip().split("\t")
        expression = elements[1]
        mirna_name = elements[0].split(",")[1]
        expression_by_mirna[mirna_name] = expression
    
with open(sys.argv[2]) as sorted_mirnas_file:
    for line in sorted_mirnas_file:
        elements = line.strip().split("\t")
        mirna_name = elements[0]
        expression = "0"
        if mirna_name in expression_by_mirna.keys():
            expression = expression_by_mirna[mirna_name]
        print mirna_name, expression

