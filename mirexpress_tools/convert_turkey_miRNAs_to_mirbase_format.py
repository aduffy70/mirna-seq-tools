#! /usr/bin/python

# convert_turkey_miRNAs_to_mirbase_format.py
# Aaron M. Duffy
# 2016-06-01

# In order to use the known turkey precursors and predicted mature miRNAs with miRExpress they need to be converted to the same format as the mirbase files that come with miRExpress.
# Precursors are easy... just put each fasta record on a single tab separated line and drop the ">".
# Mature miRNA format is (tab separated): mature_id  sequence  corresponding_precursor  start_position_of_the_miRNA_within_the_precursor
# Writes precursors to precursors_mirbase_format.txt and matures to miRNAs_mirbase_format.txt
#usage: ./convert_turkey_miRNAs_to_mirbase_format.py precursor_fastafile.fa mature_fastafile.fa

import sys
import HTSeq
import re

precursor_infile = HTSeq.FastaReader(sys.argv[1])
mature_infile = HTSeq.FastaReader(sys.argv[2])

precursor_outfile = open("precursors_mirbase_format.txt", "w")
mature_outfile = open("miRNAs_mirbase_format.txt", "w")

precursors_dict = {} #key=name, value=sequence

#Reformat the precursors, write them to the precursor outfile, and store them in the dictionary 
for precursor in precursor_infile:
    name = precursor.name
    sequence = precursor.seq    
    precursor_outfile.write(name + "\t" + sequence + "\n")
    precursors_dict[name] = sequence

#And now the mature miRNAs...
for mirna in mature_infile:
    name = mirna.name
    sequence = mirna.seq
    #Some names may have multiple names if they are associated with more than one precursor
    precursor_name = name.split("-")[0]    
    if precursor_name in precursors_dict: 
        precursor_sequence = precursors_dict[precursor_name]
    else: #it is a miRNA with a modified name because it matches more than one precursor. We need to parse the name
        precursor_name = precursor_name.split("/")[0]
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
        mature_outfile.write(name + "\t" + sequence + "\t" + precursor_name + "\t" + str(start_nt) + "\n")
    else: # the miRNA sequence wasn't found in the precursor sequence... we have a problem
        print "miRNA sequence for " + name + " wasn't found in " + precursor_name
        print sequence, precursors_dict[precursor_name]
        


precursor_outfile.close()
mature_outfile.close()
 
