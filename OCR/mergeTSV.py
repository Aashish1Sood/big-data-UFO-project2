import csv
# open final output file from assignment 1 in append mode
tsvout=open('../ufo_awesome_FINAL_OUTPUT_v2.tsv', mode='a',encoding='ISO-8859-1')

# read the ocr tsv file
with open('OCR_TSV_final.tsv',mode='r',encoding='ISO-8859-1') as ocr_tsv:
	tsvreader = csv.reader(ocr_tsv, delimiter='\t')
	next(tsvreader, None) # skip header
	#iterate through each row in ocr tsv and append it to the output of 1st assignment.
	for row in tsvreader:
		for col in row:
			tsvout.write(col + '\t')
		tsvout.write('\n')