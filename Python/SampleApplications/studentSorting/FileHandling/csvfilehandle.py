# -*- coding: utf-8 -*-

'''
what is csv file?

A CSV file (Comma Separated Values file) is a type of plain text file 
that uses specific structuring to arrange tabular data. 
Because it’s a plain text file, it can contain only actual text 
data—in other words, printable ASCII or Unicode characters.

The structure of a CSV file is given away by its name. 
Normally, CSV files use a comma to separate each specific data value. 
Here’s what that structure looks like:

'''

import csv

csvfile = "csvFile.csv"

with open(csvfile,"w") as csv_file:
	csv_writer = csv.writer(csv_file)
	# ,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	csv_writer.writerow(["s.no","Name","Age","Gender"])
	csv_writer.writerow([1,"Jon","25","M"])

with open(csvfile,"w") as csv_file:
	features = ["s.no","Name","Age","Gender"]
	csv_dict_writer = csv.DictWriter(csv_file,fieldnames=features)
	
	csv_dict_writer.writeheader()
	csv_dict_writer.writerow({"s.no":1,"Name":"John Doe","Age":100,"Gender":"M/F"})

with open(csvfile,"r") as csv_file:
	csv_reader = csv.reader(csv_file)

	for row in csv_reader:
		print row

with open(csvfile,"r") as csv_file:
	csv_dict_reader = csv.DictReader(csv_file)

	for row in csv_dict_reader:
		print row


