#!/usr/bin/env python
import os
import os.path
import json
import sys
import string
import pytesseract
import re
import difflib
import csv
import dateutil.parser as dparser
try:
	from PIL import Image, ImageEnhance, ImageFilter
except:
	print "please install PIL package"
	sys.exit()
path = sys.argv[1]

# reading file from console
img = Image.open(path)
img = img.convert('RGBA')
pix = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('temp.jpg')

# extracting text from image using tesseract
text = pytesseract.image_to_string(Image.open('temp.jpg'))
text = filter(lambda x: ord(x)<128,text)

# Initializing data variable
name = None
fname = None
dob = None
pan = None
nameline = []
dobline = []
panline = []
text0 = []
text1 = []
text2 = []


# Searching for PAN
lines = text.split('\n')
for lin in lines:
	s = lin.strip()
	s = s.rstrip()
	s = s.lstrip()
	text1.append(s)

text1 = filter(None, text1)	
#print(text1)
lineno=0

for wordline in text1:
	xx = wordline.split( )
	if ([w for w in xx if re.search('(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$', w)]):
		lineno = text1.index(wordline)
		break

text0 = text1[lineno+1:]
#print(text0)

#-----------Read Database
with open('namedb.csv', 'rb') as f:
	reader = csv.reader(f)
	newlist = list(reader)    
newlist = sum(newlist, [])

# Searching for Name and finding closest name in database
try:
	for x in text0:
		for y in x.split( ):
			if(difflib.get_close_matches(y.upper(), newlist)):
				nameline.append(x)
				break
except:
	pass

try:
	name = nameline[0]
	fname = nameline[1]
except:
	pass
	
try:
	dobline = [item for item in text0 if item not in nameline]
#	print dobline
	for x in dobline:
		z = x.split()
		z = [s for s in z if len(s) > 3]
		for y in z:
			if(dparser.parse(y, fuzzy=True)):
				dob = dparser.parse(y,fuzzy=True).year
				panline = dobline[dobline.index(x)+1:]
				break
except:
	pass
	
try:
	for wordline in panline:
		xx = wordline.split( )
		if ([w for w in xx if re.search('(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$', w)]):
			pan = panline[panline.index(wordline)+1]
			break
	pan = pan.replace(" ", "")
except:
	pass

# Making tuples of data
data = {}
data['Name'] = name
data['Father Name'] = fname
data['Date of Birth'] = dob
data['PAN'] = pan

# Writing data into JSON
with open('../result/'+ os.path.basename(sys.argv[1]).split('.')[0] +'.json', 'w') as fp:
    json.dump(data, fp)


# Removing dummy files
os.remove('temp.jpg')


'''
# Reading data back JSON(give correct path where JSON is stored)
with open('../result/'+sys.argv[1]+'.json', 'r') as f:
     ndata = json.load(f)

print "+++++++++++++++++++++++++++++++"     
print(ndata['Name'])
print "-------------------------------"
print(ndata['Father Name'])
print "-------------------------------"
print(ndata['Date of Birth'])
print "-------------------------------"
print(ndata['PAN'])
print "-------------------------------"
#'''
