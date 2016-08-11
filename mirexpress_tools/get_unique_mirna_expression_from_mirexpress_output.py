#! /usr/bin/python

# get_unique_mirna_expression_from_mirexpress_output.py
# Aaron M. Duffy
# 2016-06-07

# Which of the mirnas listed in the mirexpress expression data are actually identical miRNAs and
# are the expression levels similar?
#usage: ./get_unique_expression_from_mirexpress_output.py still_identical_mirnas_after_improving_predictions.txt mirexpress_expression_data.txt

import sys

expression_by_mirna = {} # key = mirna name, value = expression value from mirexpress
with open(sys.argv[2]) as expression_file:
    for line in expression_file:
        elements = line.strip().split("\t")
        expression = elements[1]
        mirna_name = elements[0].split(",")[1]
        expression_by_mirna[mirna_name] = expression
    
with open(sys.argv[1]) as unique_mirnas_file:
    for line in unique_mirnas_file:
        elements = line.strip().split(" ")
        sequence = elements[0]
        mirna_names = elements[1:]
        expression_values = []
        if len(mirna_names) == 1:
            print mirna_names[0], 
            if mirna_names[0] in expression_by_mirna.keys():
                print expression_by_mirna[mirna_names[0]]
            else:
                print "0"
        else:
            expression_values = []
            for name in mirna_names:
                print name,
                if name in expression_by_mirna.keys():
                    expression_values.append(expression_by_mirna[name])
                else: 
                    expression_values.append("0")
            if expression_values.count(expression_values[0]) == len(expression_values): #Are all values equal?
                print expression_values[0] + " All_equal"
            else:
                for value in expression_values:
                    print value,
                print
