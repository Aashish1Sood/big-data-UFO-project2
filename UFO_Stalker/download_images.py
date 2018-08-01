import urllib.request as req
import glob

image_urls = open('image_urls.txt','r')

count = 0
for url in image_urls:
    filename = url.replace('\n','').rsplit('/', 1)[-1]
    try:
        req.urlretrieve(url, 'images/'+filename)
    except Exception as e:
        print(e)
        print("Exception occured for URL ",url)
        print(count)
    count+=1
    if count%20 == 0:
        print(count)


l = glob.glob("./images/*")

with open("image_list","w",encoding="UTF-8") as f:
    for item in l:
        filename = item.replace('\n','').rsplit('/', 1)[-1]
        f.write(filename+'\n')

