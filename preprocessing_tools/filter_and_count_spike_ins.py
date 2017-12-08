#! /usr/bin/env python

# filter_and_count_spike_ins.py
# Given a fasta file of spike-in sequences and a fasta file of miRNA-seq reads, get read counts for each spike-in and filter those reads out of the fasta file.
# The miRNA-seq read names are in the format Samplename_######_x### where the number after the x is the number of copies of that unique sequence that were present in that sample.
# We will output 3 files:
#   A fasta file with all the reads that DO NOT match a spike-in sequence
#   A csv file showing which reads matched to which spike-in (for troubleshooting)
#   A csv file showing readcounts for each spike-in in each sample

# Aaron M. Duffy
# 2017-12-06

# usage:
# filter_and_count_spike_ins.py spike-in_file.fa reads_file.fa string_to_identify_output_files

import sys
import HTSeq

spikein_file = HTSeq.FastaReader(sys.argv[1])
reads_file = HTSeq.FastaReader(sys.argv[2])
run_id = sys.argv[3] # we will stick this run id on the front of our output file names
spikein_counts = {} # key = spikein sequence, value = dictionary with key=sample and value = readcount for that spikein in that sample
samples = [] #Keep a list of the samples as we process them, so we can use it to put the summary table in a meaningful order at the end

# Build dictionary of spikeins to compare reads against
spikeins = {} # key=sequence, value=name
for read in spikein_file:
    spikeins[read.seq] = read.name

# Compare each read against each of the spikeins
nonspikein_reads_file = open(run_id + "_nonspikein_reads.fa", "w")
spikein_to_read_file = open(run_id + "_spikein_to_read_matching.csv", "w")
spikein_to_read_file.write("Read,Read_sequence,Spike_in,Spike_in_sequence\n")
for read in reads_file:
    match_found = False
    matching_spikein = ""
    for spikein in spikeins.keys():
        if not match_found: #No reason to keep making comparisons once we've found a spike-in that matches the read
            if len(spikein) < len(read.seq):
                # The read sequence is longer. See if the spike-in sequence is within it
                if spikein in read.seq: #it's a match
                    matching_spikein = spikein
                    match_found = True
            else: # The spike-in sequence is longer. See if the read sequence is within it
                if read.seq in spikein: # it's a match
                    matching_spikein = spikein
                    match_found = True
    if match_found:
        # We found a match, so keep track of the read counts and output info about the match.
        read_count = int(read.name.split("_x")[-1])
        spikein_to_read_file.write("%s,%s,%s,%s\n" % (read.name, read.seq, spikeins[matching_spikein], matching_spikein))
        read_sample = read.name.split("_")[0]
        if read_sample not in samples:
            samples.append(read_sample)
        if matching_spikein in spikein_counts.keys():
            if read_sample in spikein_counts[matching_spikein].keys():
                spikein_counts[matching_spikein][read_sample] += read_count
            else:
                spikein_counts[matching_spikein][read_sample] = read_count
        else:
            spikein_counts[matching_spikein] = {}
            spikein_counts[matching_spikein][read_sample] = read_count
        match_found = False
        matching_spikein = ""
    else:
        #No match, put the read in the non-spikeins fasta file
        nonspikein_reads_file.write(">" + read.name + "\n" + read.seq + "\n")
nonspikein_reads_file.close()
spikein_to_read_file.close()

#Build a table of readcounts by sample for each spikein
read_count_file = open(run_id + "_spikein_read_counts_by_sample.csv", "w")
header_string = "Spike_in,Sequence"
for sample in sorted(samples):
    header_string += "," + sample
read_count_file.write(header_string + "\n")
for spikein in spikein_counts.keys():
    print_string = spikeins[spikein] + "," + spikein
    for sample in sorted(samples):
        if sample in spikein_counts[spikein].keys():
            print_string += "," + str(spikein_counts[spikein][sample])
        else:
            print_string += ",0"
    read_count_file.write(print_string + "\n")
read_count_file.close()
