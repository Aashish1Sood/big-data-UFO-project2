import pickle
import csv

with open("final.pickle","rb") as f1:
    l = pickle.load(f1)
print(len(l))
print(l[0])
print(l[-1])

fourteen_tab = "\t" * 14
five_tab = '\t' * 5
with open("my.tsv", "w", encoding="UTF-8") as f:
    for item in l:
        if "Date of Sighting" in item:
            f.write(item['Date of Sighting'])
        f.write("\t\t")
        if "geo" in item and item["geo"][0] != None:
            lat_long_list = item["geo"][1].split(",")
            f.write(item['geo'][0] + "\t\t\t\t" + lat_long_list[0] + "\t" + lat_long_list[1])
        else:
            f.write(five_tab)
        f.write(fourteen_tab)
        if 'filename' in item:
            f.write(item['filename'])
            print(item['filename'])
        f.write("\t")
        if 'Obj_rec' in item:
            f.write(item['Obj_rec'])
        f.write("\t")
        if 'obj_cap' in item:
            f.write(item['obj_cap'])
        f.write("\n")

# open final output file from assignment 1 in append mode
tsvout=open('../ufo_awesome_FINAL_OUTPUT_v2.tsv', mode='a',encoding='ISO-8859-1')

# read the ocr tsv file
with open('my.tsv',mode='r',encoding='ISO-8859-1') as ocr_tsv:
	tsvreader = csv.reader(ocr_tsv, delimiter='\t')
	#next(tsvreader, None) # skip header
	#iterate through each row in ocr tsv and append it to the output of 1st assignment.
	for row in tsvreader:
		for col in row:
			tsvout.write(col + '\t')
		tsvout.write('\n')