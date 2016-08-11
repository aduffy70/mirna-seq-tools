#! /usr/bin/python

# get_length_distribution_from_mirdeep2_fasta.py
# Aaron M. Duffy
# 2016-05-27

# Builds a table of counts of unique and total reads with each readlength. Assumes mirdeep2 formatted names.

#usage: ./get_length_distribution_from_mirdeep2_fasta.py fastafile.fasta

import sys
import HTSeq

fasta_file = HTSeq.FastaReader(sys.argv[1])
length_counts = {} #dictionary of lists [unique_count, total_count] for each readlength

for read in fasta_file:
    length = len(read.seq)
    count = int(read.name.split("_x")[1])
    if length not in length_counts.keys():
        length_counts[length] = [0, 0]
    length_counts[length][0] += 1
    length_counts[length][1] += count
print "Length\tUnique\tTotal"
for length in length_counts.keys():
    print "%s\t%s\t%s" % (length, length_counts[length][0], length_counts[length][1])
        
