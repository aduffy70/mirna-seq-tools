#! /usr/bin/python

# collapse_all_combined_reads_in_mirexpress_format.py
# Aaron M. Duffy
# 2016-06-02

# I combined all the *.trimmed18 files into one so now it has many duplicates. Combine them.
#usage: ./collapse_all_combined_reads_in_mirexpress_format.py all_samples.trimmed18

import sys

read_counts = {} #dictionary of counts for each unique read

with open(sys.argv[1]) as infile:
    for line in infile:
        count = int(line.strip().split("\t")[0])
        sequence = line.strip().split("\t")[1]
        if sequence in read_counts:
            read_counts[sequence] += count
        else:
            read_counts[sequence] = count
for read in read_counts.keys():
    print str(read_counts[read]) + "\t" + read

