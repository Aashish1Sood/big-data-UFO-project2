There are 3 major sub-folders in the Assignment. 
First "OCR" to use ocr-pipeline on British UFO PDF files to extract the data and parse them into TSV, and 
Second "UFO_Stalker" for scraping the UFO stalker website to fetch the image URLs.
Third "NER". It contain Tika NER code and the input and output files.


The main input file containing the ufo data is :- 
(we took the output file from assignment 1 and renamed it _v2)
ufo_awesome_FINAL_OUTPUT_v2.tsv

The intermediate files are as following:-
OCR/OCR_TSV_final.tsv

The main modified output file containing the ufo data is :- 
ufo_awesome_FINAL_OUTPUT_v2.tsv


The libraries used/need to be installed are:-
pip install selenium
imagemagick install - https://www.imagemagick.org/script/download.php
brew install tesseract
brew install ghostscript

Information about the records in the fina TSV file:- ufo_awesome_FINAL_OUTPUT_v2.tsv
1) Record 1 - 61068 ---> Old ufo_awesome_FINAL_OUTPUT_v1 TSV records of Assignment 1
2) Record 61069 - 61207 ---> OCR records
3) Record 61208 - 66583 --> UFO stalker Image records.

The important files present in the folders are :-

1) ocr_pipeline.sh
-- Bash script to split PDF files into single page files and convert them into tiff files with high dpi resolution and improved using image enhancement techniques using imagemagick library. We then use the tesseract on each of the tiff files, and extract the data into corresponding text files.


2) OCR_parse.py
-- Python script to parse the generated text files by ocr-pipeline.sh. It looks for the following keywords in the text files:
	a. Flying or aerial (if page is of interest)
	b. Date & Sighting (for Date of Sighting)
	c. Mins, Secs, Hours, Still there (for Duration)
	d. Description (for Shape)
	e. Position (for Location)
	f. How Observed + Direction (for Description)
	g. Receipt (for Date of Report)
It then parses the data meant for each keyword. Since tesseract produced lot of uncleaned data, we had to perform manual updates to the data for the parser to parse the data properly. There are still spelling mistakes, but the data is readable and understandable.


3) MergeTSV.py
-- Python script to append the new sighting rows from OCR output to the UFO final output from assignment 1. It takes TSV file with OCR rows and modifies the   UFO final output (from assignment 1) by appending these rows. 


4) url_extract[1-4].py
-- The UFO Stalker website has urls ranging from the event id 1 to event id 91148. To scrape all these events from the UFO stalker website, we have written 5 programs - url_extract.py, url_extract1.py, .... ,url_extract4.py where each program is run parallely and executes ~20000 event ids to scrape the image urls.
-- These programs give us the scraped image urls and are stored in text files - urls_images2.txt, urls_images2.txt, ... , urls_images5.txt


5) combine_urls.py
-- This program is used to take all the scraped urls_images[1-5].txt files and combine them all and store just the unique ones in the file image_urls.txt. This new text file is in turn used  for Image captioning and object recognition.


6) download_images.py
-- This python script downloads all the images from the scraped URL's and generate a file with list of filenames which will be passed to genCapAndObj.java


7) genCapAndObj.java
-- This java code takes the list of all the image filenames and the downloaded images in the previous step as input. Then it generates following three features
a) Recognized Objects :- This is done using Object Recognition Docker
b) Image Captions :- This done using the corresponding Image Captioning Docker.
c) Metadata Features :- Date of Sighting, Geolocation.
This program generates the features and populates it in an output file :- final_list


8) Featurizer.py
-- This python script works on the featurized file(final_list) and generates a pickle file containing properly formatted features. It does the requires date/timestamp formatting, generating geolocation and string formatting of the image captions.


9)MergeFeatures.py
-- This python scipt merges the the features generated from OCR pipeline with the Object recognition and Image captioning features into one TSV

10) tikaNER.java
-- This java code generates four NER features(NER_PERSON, NER_LOCATION, NER_ORGANIZATION, NER_DATE) from the Description column of the dataset. We used Apache OpenNLP for NER tagging.
Once the Tika features were generated they were merged with the final TSV

The order in which the programs need to be executed:
1) ocr_pipeline.sh 
2) OCR_parse.py
3) MergeTSV.py
4) url_extract[1-4].py
5) combine_urls.py
6) download images.py
7) genCapAndObj.java
8) Featurizer.py
9) MergeFeatures.py
10) tikaNER.java
