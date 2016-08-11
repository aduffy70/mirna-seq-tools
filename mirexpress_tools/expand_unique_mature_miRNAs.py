#! /usr/bin/python

# expand_unique_mature_miRNAs.py
# Aaron M. Duffy
# 2016-06-02

# I want all of the exactly identical reference mature miRNAs to map to all of the precursors they could have
# come from, so I need to expand the unique mature miRNAs and get their starting locations for each precursor
# to which they were derived.
#usage: ./expand_unique_mature_miRNAs.py precursor_fastafile.fa unique_mature_mirbase_format_file.txt

import sys
import HTSeq
import re

precursor_infile = HTSeq.FastaReader(sys.argv[1])


precursors_dict = {} #key=name, value=sequence

#store the precursors in the dictionary. We'll need them to map miRNAs against 
for precursor in precursor_infile:
    name = precursor.name
    sequence = precursor.seq    
    precursors_dict[name] = sequence

multiples_count = 0 #keep track of which miRNAs were part of the each group of identical miRNAs
with open(sys.argv[2]) as mature_infile:
    for line in mature_infile:
        sequence = line.split("\t")[1]
        mirna_name = line.split("\t")[0]
        mirna_name_elements = mirna_name.split("/")
        if len(mirna_name_elements) == 1: #It is a single miRNA, no processing needed
            print line.strip()
        else:
            multiples_count += 1
            for name in mirna_name_elements: #...for each miRNA name within the combined name...
                precursor_name = name.split("-")[0]
                p_3_or_5 = name.split("-")[1]
                if "ENSMGAG" in precursor_name:
                    prefix = "ENSMGAG"
                    suffix = precursor_name[7:]
                else:
                    prefix = "URS"
                    suffix = precursor_name[3:]
                search_string = prefix + "[0]*" + suffix
                real_name = "NOMATCH" # If we don't find it, it will stay NOMATCH, otherwise, this will be replaced with the real name
                for precursor_long_name in precursors_dict.keys():
                    matchObj = re.match(search_string, precursor_long_name)
                    if matchObj:
                        real_name = precursor_long_name
                precursor_name = real_name
                # find where the miRNA aligns to the precursor
                if sequence in precursors_dict[precursor_name]:
                    start_nt = precursors_dict[precursor_name].index(sequence) + 1 #We want the start index but python counts from zero
                    # write it all to the file
                    print precursor_name + "-" + p_3_or_5 + "_" + str(multiples_count) + "\t" + sequence + "\t" + precursor_name + "\t" + str(start_nt)
                else: # the miRNA sequence wasn't found in the precursor sequence... we have a problem
                    print "miRNA sequence for " + name + " wasn't found in " + precursor_name
                    print sequence, precursors_dict[precursor_name]
        
