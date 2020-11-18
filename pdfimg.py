#! python3
# pdfimg.py - Converts PDF files to image files

import sys, os
import fitz # fitz is actually PyMuPDF

if len(sys.argv) != 3:
	print('Usage: pdfimg.py [file] [Option]')
	print('Option: 0 - Rough convert every page')
	print('        1 - Create folder and extract raw images from each page')
	sys.exit
	quit()

path = os.getcwd() + "\\" # current working directory

# set variables from arguments

filename = sys.argv[1]

filepath = path + filename

outputpath = path + 'test.png'

nameonly = filename[:-4]

extractpath = path + nameonly + " extracted" + "\\"

# clean up "options" variable

try:
	option = sys.argv[2]
	option = int(option)
except:
	print("something went wrong, exiting")
	quit()

if option == 0:
	print("Rough converting pages to png!")
elif option == 1:
	print("Extracting raw images!")
else:
	print("something went wrong, exiting")
	quit()

# direct convert (choice a)

''' OLD METHOD USING pdf2image
if option == 0:
	pages = convert_from_path(filepath, 150)
	
	i=0
	
	for page in pages:
		i += 1
		id = "{:04d}".format(i) # format current i value to string with leading zeros
		page.save('{}-{}.jpg'.format(nameonly,id), 'JPEG')
'''

if option == 0:
	doc = fitz.open(filepath)
	
	i=0
	
	for page in doc:
		i += 1
		id = "{:04d}".format(i) # format current i value to string with leading zeros
		print(page, i)
		image_matrix = fitz.Matrix(fitz.Identity)
		image_matrix.preScale(2, 2)
		pix = page.getPixmap(alpha = False, matrix=image_matrix)
		pix.writePNG('{}-{}.png'.format(nameonly,id))


# extract images (choice b)
# this was a direct copy from stackoverflow lmao

if option == 1: 
	try: #creath path, if it already exists it will error for some reason
		os.mkdir(extractpath)
	except:
		pass
	doc = fitz.open(filepath)
	total = 0
	fuck = 0 # counter for images that are not RGB or CMYK
	for i in range(len(doc)):
		for img in doc.getPageImageList(i):
			total += 1
			xref = img[0]
			pix = fitz.Pixmap(doc, xref)
			if str(pix.colorspace) == str(fitz.csRGB) or str(pix.colorspace) == str(fitz.csGRAY):
				pix.writePNG(extractpath + "p%s-%s.png" % (i, xref))
			elif str(pix.colorspace) == str(fitz.csCMYK):  # CMYK: convert to RGB first
				pix1 = fitz.Pixmap(fitz.csRGB, pix)
				pix1.writePNG(extractpath + "p%s-%s.png" % (i, xref))
				pix1 = None
			else:
				print("It is neither RGB or CMYK!")
				fuck += 1
			pix = None
	print("{} out of {} images were not RGB nor CMYK".format(fuck,total))



