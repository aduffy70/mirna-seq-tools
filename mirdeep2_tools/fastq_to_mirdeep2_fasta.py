#! /usr/bin/python

# fastq_to_mirdeep2_fasta.py
# Aaron M. Duffy
# 2016-05-20

# Converts fastq data to fasta but with the description line in the format required by mirdeep2.
# example:
# >E10_123456_x1
# Where the first part is a 3 letter code for the sample, the second part is a unique (to the
# sample) integer identifying the read, and the third part starts with an x and tells how many
# times the read is present in the sample (I'm using all ones since I haven't collapsed the 
# reads yet).

#usage: ./fastq_to_mirdeep2_fasta.py fastqfile.fastq Three_letter_code_text

import sys
import HTSeq

unique_id = 0
fastq_file = HTSeq.FastqReader(sys.argv[1])
three_letter_code = sys.argv[2]

for read in fastq_file:
    sequence = read.seq
    unique_id += 1
    description = ">" + three_letter_code + "_" + str(unique_id) + "_x1"
    print description
    print sequence
 
