urls_files = ["urls_images1.txt","urls_images2.txt","urls_images3.txt","urls_images4.txt","urls_images5.txt"]

#reading the individual image url text files created by the programs and combining it into a single txt file
final_image_urls = open("image_urls.txt",'w')
url_set = set()
for url in urls_files:
	f = open(url,'r')
	for row in f:
		if(row not in url_set):
			final_image_urls.write(row)
			url_set.add(row)


