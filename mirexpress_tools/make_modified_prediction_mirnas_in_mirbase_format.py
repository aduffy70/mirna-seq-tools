#! /usr/bin/python

# make_modified_prediction_mirnas_in_mirbase_format.py
# Aaron M. Duffy
# 2016-06-06

# Make a new mirbase format file with the modified predicted miRNA based on the final dispositions.
# usage: ./make_modified_prediction_mirnas_in_mirbase_format.py final_dispositions_file.txt old_mature_mirna_mirbase_file.txt precursors_mirbase_file.txt

import sys

precursors = {} # key=precursor name, value=sequence

with open(sys.argv[3]) as precursor_file:
    for line in precursor_file:
        name = line.split("\t")[0]
        sequence = line.strip().split("\t")[1]
        precursors[name] = sequence

to_be_changed = {} #key=mature name, value = (old position, new position)

with open(sys.argv[1]) as disposition_file:
    for line in disposition_file:
        disposition = line.strip().split(" ")[4]
        if disposition == "small_supported_change" or disposition =="manual_change":
            name = line.split(" ")[0]
            old_position = int(line.split(" ")[1])
            new_position = int(line.split(" ")[2])
            to_be_changed[name] = (old_position, new_position)

with open(sys.argv[2]) as old_mature_file:
    for line in old_mature_file:
        elements = line.strip().split("\t")
        short_name = elements[0].split("_")[0] #Some names have a suffix (to indicate mirnas with identical sequence) that isn't actually part of the name
        precursor_name = elements[2]
        if precursor_name != short_name.split("-")[0]: #Quick check to make sure something unexpected hasn't happened
            print "The precursor name and mature mirna names don't match!"
        if short_name in to_be_changed: #This is one we want to change
            new_position = to_be_changed[short_name][1]
            old_position = to_be_changed[short_name][0]
            if old_position != int(elements[3]): #Quick check to make sure something unexpected hasn't happened.
                print "The old position in the disposition doesn't match the position in the mirbase file!"
            new_sequence = precursors[precursor_name][new_position - 1: new_position + 21] #Get the 22 base sequence from the precursor sequence
            old_sequence = precursors[precursor_name][old_position - 1: old_position + 21] 
            if old_sequence != elements[1]: #Quick check to make sure something unexpected hasn't happened
                print old_sequence, elements[1], " The old sequence from disposition file and the mature mirbase file don't match!"
            print "%s_mod\t%s\t%s\t%s" % (elements[0], new_sequence, precursor_name, new_position)
        else: #No change needed, print the line as is.
            print line.strip()
