#! /usr/bin/python

# find_still_identical_mirnas_after_improving_predictions.py
# Aaron M. Duffy
# 2016-06-07

# After improving mirna predictions based on mirexpress output, some previously identical miRNAs may now
# be different and some previously different miRNAs may now be identical. Check.
#usage: ./find_still_identical_mirnas_after_improving_predictions.py improved_mature_miRNAs_in_mirbase_format.txt

import sys

unique_mirnas = {} # key=sequence value=list of mirna names
with open(sys.argv[1]) as infile:
    for line in infile:
        elements = line.strip().split("\t")
        sequence = elements[1]
        mirna_name = elements[0]
        if sequence in unique_mirnas:
            unique_mirnas[sequence].append(mirna_name)
        else:
            unique_mirnas[sequence] = [mirna_name]
for sequence in unique_mirnas.keys():
#    if len(unique_mirnas[sequence]) > 1: #just print non-unique mirnas
    print sequence,
    for mirna in unique_mirnas[sequence]:
        print mirna,
    print ""
