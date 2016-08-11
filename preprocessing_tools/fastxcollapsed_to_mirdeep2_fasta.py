#! /usr/bin/python

# fastxcollapsed_to_mirdeep2_fasta.py
# Aaron M. Duffy
# 2016-05-24

# Converts fasta description line to the format required by mirdeep2.
# example:
# >123456-18 becomes >E10_123456_x18
# Where the first part is a 3 letter code for the sample, the second part is a unique (to the
# sample) integer identifying the read, and the third part starts with an x and tells how many
# times the read is present in the sample.

#usage: ./fastxcollapsed_to_mirdeep2_fasta.py fastafile.fasta Three_letter_code_text

import sys
import HTSeq

fasta_file = HTSeq.FastaReader(sys.argv[1])
three_letter_code = sys.argv[2]

for read in fasta_file:
    sequence = read.seq
    name_and_count = read.name.split("-")
    new_description = ">" + three_letter_code + "_" + name_and_count[0] + "_x" + name_and_count[1]
    print new_description
    print sequence
 
