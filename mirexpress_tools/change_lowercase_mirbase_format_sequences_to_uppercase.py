#! /usr/bin/python

# change_lowercase_mirbase_format_sequences_to_uppercase.py
# Aaron M. Duffy
# 2016-06-27

# mirdeep outputs novel mirna sequences in lowercase letters but mirexpress wants the mirbase formatted files in uppercase.
#usage: ./change_lowercase_mirbase_format_sequences_to_uppercase.py lowercase_mirbase_format_file.txt

import sys

with open(sys.argv[1]) as lower_case_file:
	for line in lower_case_file:
		line = line.strip()
		uppercase_line = ""
		for letter in line:
			if letter == "c":
				uppercase_line += "C"
			elif letter == "u":
				uppercase_line += "U"
			elif letter == "g":
				uppercase_line += "G"
			elif letter == "t":
				uppercase_line += "T"
			elif letter == "a":
				uppercase_line += "A"
			elif letter == "n":
				uppercase_line += "N"
			else:
				uppercase_line += letter
		print uppercase_line
