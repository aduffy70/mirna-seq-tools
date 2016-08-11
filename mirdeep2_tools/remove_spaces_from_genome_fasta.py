#! /usr/bin/python

# remove_spaces_from_genome_fasta.py
# Aaron M. Duffy
# 2016-05-23

# mirdeep2 doesn't like spaces in the genome fasta descriptions. Remove everything from the first space on (this leaves the
# genbank sequence designator).

#usage: ./remove_spaces_from_genome_fasta.py NCBI_genome_fastafile.fa

import sys
import HTSeq

fasta_file = HTSeq.FastaReader(sys.argv[1])

for read in fasta_file:
    name_no_spaces = read.name.split(" ")[0]    
    print ">" + name_no_spaces
    print read.seq
 
