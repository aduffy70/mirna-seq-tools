#! /usr/bin/python

# remove_under_18_bp_from_mirExpress_format.py
# Aaron M. Duffy
# 2016-06-02

# miRExpress keeps reads 15bp or longer but with the settings I am using everything under 18bp gets put in the "Others"
# so it won't get included in the expression analysis anyway. Removing those 15-17bp reads will speed up processing and
# make for cleaner alignment output files so let's manually remove them.
# The trimmed files are in a format with the number of read copies and the sequences tab-separated.
#usage: ./remove_under_18_bp_from_mirExpress_format.py trimmed_reads_file_in_mirexpress_format.trimmed15

import sys

#under_18_count = 0
with open(sys.argv[1]) as infile:
    for line in infile:
        sequence = line.strip().split("\t")[1]
        if len(sequence) >= 18:
            print line.strip()
#        else:
#            under_18_count += 1
#print "%s unique reads removed" % str(under_18_count)
#I checked this count and it matches the combined counts of unique reads length 15 + 16 + 17 in the read_statistics output.
