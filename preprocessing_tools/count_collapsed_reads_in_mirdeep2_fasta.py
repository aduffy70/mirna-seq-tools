#! /usr/bin/python

# count_collapsed_reads_in_mirdeep_fasta.py
# Aaron M. Duffy
# 2016-05-24

# Once you've collapsed reads you can't use wc -l fastafile.fa / 2 to count reads--it gives
# the number of unique reads. This script gets the actual read count for files formatte for
# mirdeep2.

#usage: ./count_collapsed_reads_in_mirdeep2_fasta.py fastafile.fasta

import sys
import HTSeq

fasta_file = HTSeq.FastaReader(sys.argv[1])
total_count = 0
unique_count = 0

for read in fasta_file:
    count = int(read.name.split("_x")[1])
    total_count += count
    unique_count += 1
print "Unique: %s    Total:%s" % (unique_count, total_count)

