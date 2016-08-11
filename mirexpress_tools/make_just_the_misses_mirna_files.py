#! /usr/bin/python

# make_just_the_misses_mirna_files.py
# Aaron M. Duffy
# 2016-06-06

# 102 precursor miRNAs aren't included in the mirexpress output. Some precursors with no mapped reads DO get
# included so I don't know why these didn't. I want to rerun mirexpress using just these so I need a script
# to make precursor and mature mirna files in mirbase format with just these 102 precursors and the 
# corresponding predicted mature miRNAs.

# Usage: make_just_the_misses_mirna_files.py list_of_precursors_file.txt precursors_in_mirbase_format.txt mature_in_mirbase_format.txt

import sys

missed_list = [] #list of precursor miRNAs we want included in the output
with open(sys.argv[1]) as list_file:
    for line in list_file:
        missed_list.append(line.strip())

with open(sys.argv[2]) as precursor_file:
    for line in precursor_file:
        if line.split("\t")[0] in missed_list:
            print line.strip()

with open(sys.argv[3]) as mature_file:
    for line in mature_file:
        if line.split("-")[0] in missed_list:
            print line.strip()     
