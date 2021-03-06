#!/usr/bin/python3


import sys, re

if len(sys.argv) > 1:
    input_file = sys.argv[1]
    input_citation_file = sys.argv[2]
else:
    input_file = "pmid_annotations.tzt"
    input_citation_file = "pmid_citations.txt"

input_file_trimmed = re.sub(r'^[\.]','',re.sub(r'[^a-zA-Z0-9i\_\.]', '', input_file))
input_citation_file_trimmed =  re.sub(r'^[\.]','',re.sub(r'[^a-zA-Z0-9\_\.]', '', input_citation_file))

input_file_medline_pmids = "pmid_list.txt"
output_file = input_file_trimmed + "_" + input_citation_file_trimmed + "_" + "neighborhood_annotation_statistics_all_medline.txt"

print("Reading a list of PMIDs...")
# read a list of all MEDLINE PMIDs
f_in = open(input_file_medline_pmids, "r")

pmids_medline = {}
for line in f_in:
    line = line[:-1]
    pmid = line
    pmids_medline[pmid] = 1

# read a list of annotations
f_in = open(input_file, "r")

print("Reading annotations...")
annotations_pmid = {}
pmids = {}
counter_annotations=0
for line in f_in:
    line = line[:-1]
    data = line.split("\t")
    pmid = data[0]
    if pmid != "":
        # create a dictionary of annotations for each PMID
        annotations_pmid[pmid] = data[1]
        pmids[pmid] = 1
        for annotation in annotations_pmid[pmid].split("|"):
            counter_annotations += 1

print("Annotations read: " + str(counter_annotations))
print("PMIDs read: " + str(len(pmids.keys())))

counter=0
pmid_connections = {}

print("Reading citation data...")

# read the file with citation data, which is a list of PMID pairs
f_in = open(input_citation_file)

all_connection_count = {}
annotated_connection_count = {}
for line in f_in:
    data = line[:-1].split("\t")
    counter+=1
    if (counter / 100000000) == int(counter / 100000000):
        print("Read " + str(counter) + " connections.")
    if len(data) > 1:
        # for each pair of PMIDs
        pmid1 = data[0]
        pmid2 = data[1]
        # check if the first PMID is annotated
        if pmid1 in pmids.keys():
            if pmid2 in annotated_connection_count.keys():
                annotated_connection_count[pmid2] += 1
            else:
                annotated_connection_count[pmid2] = 1
        # do the same but now in reverse
        if pmid2 in pmids.keys():
            if pmid1 in annotated_connection_count.keys():
                annotated_connection_count[pmid1] += 1
            else:
                annotated_connection_count[pmid1] = 1

annotated_count_list = {}
all_count_list = {}

annotated_count_list[0] = 0
all_count_list[0] = 0

# go back to each PMID and count statistics on number of annotated and not-annotated neighbors
for pmid in pmids_medline.keys():
    # statistics on annotated neighbors
    if pmid in annotated_connection_count.keys():
        count = annotated_connection_count[pmid]
        if count in annotated_count_list.keys():
            annotated_count_list[count] += 1
        else:
            annotated_count_list[count] = 1
    else:
        count = 0
        annotated_count_list[count] += 1
    # statistics on non-annotated neighbors
    if pmid in all_connection_count.keys():
        count = all_connection_count[pmid]
        if count in all_count_list.keys():
            all_count_list[count] += 1
        else:
            all_count_list[count] = 1
    else:
        count = 0
        all_count_list[count] += 1

total_pmids = len(pmids_medline.keys()) 

# Write statistics output in a table
print("Writing output to " + output_file + "...")

f_out = open(output_file, "w")

f_out.write("Connection count" + "\t" + "With annotated connections" + "\t" + "Percentage of all records\n")
print("Connection count" + "\t" + "With annotated connections" + "\t" + "Percentage of all records")

for i in range(0,max(annotated_count_list.keys())+1):
    if i in annotated_count_list.keys():
        annotated_count = annotated_count_list[i]
        percentage_annotated_count = annotated_count_list[i] / total_pmids
    else:
        annotated_count = 0
        percentage_annotated_count = 0
    f_out.write(str(i) + "\t" + str(annotated_count) + "\t" + str(percentage_annotated_count) + "\n")
    if i <= 20:
        print(str(i) + "\t" + str(annotated_count) + "\t" + str(percentage_annotated_count))
