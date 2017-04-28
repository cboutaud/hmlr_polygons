# -*- coding: utf-8 -*-
# In addition to having bs4 and requests installed you'll also need to install lxml and create a folder called "zipfiles" in the main repo to run this script
from bs4 import BeautifulSoup
import requests

# The HM Land registry as a page with links to individual pages for each LAs which contains a download link for a zipfile containing that LA's polygons

# Base url for goverment pages
url_base = "https://www.gov.uk" 

# getting the links to individual pages for each LAs
url_page = "/government/collections/download-inspire-index-polygons"
url = url_base + url_page

# Using request to access the page and BeautifulSoup to search the page content for the information we need.
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")
titles = soup.find_all("h3", class_="group-document-list-item-title")
links = [title.find('a')['href'] for title in titles]

# getting  the download links
for index, link in enumerate(links):
	# index/break loop always useful for testing
	# if index >= 5:
	# 	break

	# Keep track while running code 
	print "Extrating zip " + str(index+1) + "/" + str(len(links)) + "."

	# See line 15
	url = url_base + link
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "lxml")
	dl_link = soup.find("p", class_="metadata").find('span', class_="url").get_text()

	# set a variable to name the files and get rid of welsh names (sorry :/, but it's more clear) (i.e. Abertawe_-_Swansea.zip -> Swansea.zip)
	filename = dl_link.split('/')[3]
	if '_-_' in filename:
		filename = filename.split('_-_')[1]

	# get the zipfile and set a path for where to save it on computer
	r = requests.get(dl_link, stream=True)
	file_path = "zipfiles/" + filename

	# this writes large zipfiles chunk by chunk
	with open(file_path, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
