# -*- coding: utf-8 -*-
# In addition to having glob and zipfile installed you'll also need to create a folder called "gmlfiles" in the main repo to run this script
import glob, zipfile

# with the zipfiles in one folder we can use glob to open them and extract the GMLs containing the polygons to a new folder
zipfiles = glob.glob("zipfiles/*.zip")

for index, file in enumerate(zipfiles):
	# Keep track while running code 
	print "Extrating zip " + str(index+1) + "/" + str(len(zipfiles)) + "."

	zf = zipfile.ZipFile(file, "r")
	output_name = file[9:-4]
	
	# we don't want to download the PDFs so we will check the namelist for the GMLs only instead of using the extractall() method
	for name in zf.namelist():
		if name[-3:] == "gml":
			data = zf.read(name)
			output = open("gmlfiles/" + output_name + ".gml", "wb")
			output.write(data)
			output.close()
	zf.close()
