#! /usr/bin/python

# parse_mirexpress_read_align_file.py
# Aaron M. Duffy
# 2016-06-02

# Use mirexpress read align output file to improve turkey miRNA predictions. For various reasons, not all predicted
# mature miRNAs end up in the read_align output, so we will also read in the mature miRNA mirbase format file.
#usage: ./parse_mirexpress_read_align_file.py read_align_file.txt mature_miRNAs_in_mirbase_format.txt

import sys
import operator

precursor_sequence_is_next = False
is_5p_section = False
is_3p_section = False
is_other_section = False
starts_5p = {} # key=start position, value=read count
starts_3p = {} # key=start position, value=read count
read_count_5p = 0
read_count_3p = 0
predicted_5p_start = 0
predicted_3p_start = 0
#Keep track of the counts of reads with each final disposition
disp_no_data = 0 # no data to change or support original miRNA prediction
disp_supports_prediction = 0 # miRNA-seq data supports the original miRNA prediction
disp_small_change = 0 # Small change from the prediction (<=6bp shift) with strong support (>50% of reads and >=4 reads support change)
disp_needs_eval = 0 # Large change or weak support. I'll evaluate manually.
total_precursors = 0 #Track how many precursors get processed

predicted_positions = {} # key=precursor_name value=[predicted_5p_start, predicted_3p_start]
with open(sys.argv[2]) as mirbase_file:
    for line in mirbase_file:
        line_elements = line.strip().split("\t")
        precursor_name = line_elements[0].split("-")[0]
        if precursor_name not in predicted_positions.keys():
            predicted_positions[precursor_name] = [0, 0]
        if "-5p" in line_elements[0]:
            predicted_positions[precursor_name][0] = int(line_elements[3])
        else:
            predicted_positions[precursor_name][1] = int(line_elements[3])

# Keep track of which precursors not included in the output (these presumable have no reads mapped to them... but there are also a few precursors with no reads mapped to them that ARE in the output so I want to investigate further to make sure I don't have precursors not being included in the analysis for some unknown reason)
unused_precursors = predicted_positions.keys()

with open(sys.argv[1]) as alignment_infile:
    for line in alignment_infile:
        line = line.rstrip()
        if line[0:3] == "ENS" or line[0:3] == "URS": #first line of a precursor record
            total_precursors += 1
            precursor_name = line
            predicted_5p_start = predicted_positions[precursor_name][0]
            predicted_3p_start = predicted_positions[precursor_name][1]
            precursor_sequence_is_next = True
            if precursor_name in unused_precursors:
                unused_precursors.remove(precursor_name)
        elif precursor_sequence_is_next: #This line contains the precursor sequence
            precursor_sequence = line
            precursor_sequence_is_next = False
        elif "-5p" in line: #Starting into the -5p reads
            is_5p_section = True
            is_3p_section = False
        elif "-3p" in line: #Starting into the -3p reads
            is_3p_section = True
            is_5p_section = False
        elif "Others" in line: #Starting into the Other reads
            is_other_section = True
            is_5p_section = False
            is_3p_section = False
        elif "//" in line: #end of the precursor record
            if len(starts_5p) > 0:
                new_start_5p = sorted(starts_5p.items(), key=operator.itemgetter(1), reverse=True)[0][0]
                new_start_5p_count = starts_5p[new_start_5p]
                print "%s-5p %s %s (%s/%s)" % (precursor_name, predicted_5p_start, new_start_5p, new_start_5p_count, read_count_5p),
                if new_start_5p == predicted_5p_start:
                    disp_supports_prediction += 1
                    print "prediction_supported"
                elif abs(new_start_5p - predicted_5p_start) <= 6 and new_start_5p_count / float(read_count_5p) > 0.5 and new_start_5p_count >= 4:
                    disp_small_change += 1
                    print "small_supported_change"
                else:
                    disp_needs_eval += 1
                    print "manual_"
                    for position in sorted(starts_5p.keys()):
                        print position, starts_5p[position]
            else:
                disp_no_data += 1
                print "%s-5p %s %s (0/0) no_data" % (precursor_name, predicted_5p_start, predicted_5p_start)
            if len(starts_3p) > 0:
                new_start_3p = sorted(starts_3p.items(), key=operator.itemgetter(1), reverse=True)[0][0]
                new_start_3p_count = starts_3p[new_start_3p]
                print "%s-3p %s %s (%s/%s)" % (precursor_name, predicted_3p_start, new_start_3p, new_start_3p_count, read_count_3p),
                if new_start_3p == predicted_3p_start:
                    disp_supports_prediction += 1
                    print "prediction_supported"
                elif abs(new_start_3p - predicted_3p_start) <= 6 and new_start_3p_count / float(read_count_3p) > 0.5 and new_start_3p_count >= 4:
                    disp_small_change += 1
                    print "small_supported_change"
                else:
                    disp_needs_eval += 1
                    print "manual_"
                    for position in sorted(starts_3p.keys()):
                        print position, starts_3p[position]
            else:
                disp_no_data += 1
                print "%s-3p %s %s (0/0) no_data" % (precursor_name, predicted_3p_start, predicted_3p_start)
            #Reset so we are ready for the next precursor
            read_count_5p = 0
            read_count_3p = 0
            starts_5p = {}
            starts_3p = {}
            predicted_5p_start = 0
            predicted_3p_start = 0
            is_5p_section = False
            is_3p_section = False
            is_other_section = False
        elif len(line.lstrip().split(" ")) == 2: #It's a read/count line
            start_pos = 1 + len(line) - len(line.lstrip())
            read_count = int(line.lstrip().split(" ")[1])
            if is_5p_section:
                if start_pos in starts_5p:
                    starts_5p[start_pos] += read_count
                else:
                    starts_5p[start_pos] = read_count
                read_count_5p += read_count
            if is_3p_section:
                if start_pos in starts_3p:
                    starts_3p[start_pos] += read_count
                else: 
                    starts_3p[start_pos] = read_count
                read_count_3p += read_count
            if is_other_section: # Determine whether it is closer to the predicted 5p or 3p start 
                distance_to_5p = abs(predicted_5p_start - start_pos)
                distance_to_3p = abs(predicted_3p_start - start_pos)
                if distance_to_5p < distance_to_3p: #call it a 5p read
                    if start_pos in starts_5p:
                        starts_5p[start_pos] += read_count
                    else: 
                        starts_5p[start_pos] = read_count
                    read_count_5p += read_count
                else: #call it a 3p (I know, this will also be true if the distance is equal, but if it ends up affecting the predicted start position it will be a big shift that I'll have to investigate manually anyway.)
                    if start_pos in starts_3p:
                        starts_3p[start_pos] += read_count
                    else:
                        starts_3p[start_pos] = read_count
                    read_count_3p += read_count
print "No data", disp_no_data
print "Supports prediction", disp_supports_prediction
print "Small change", disp_small_change
print "Need evaluation", disp_needs_eval
print "Total", total_precursors

print "Precursors not included in output:"
for precursor in unused_precursors:
    print precursor
