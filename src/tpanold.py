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
from PIL import Image, ImageEnhance, ImageFilter

path = sys.argv[1]

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


lines = text.split('\n')
for lin in lines:
	s = lin.strip()
	s = s.rstrip()
	s = s.lstrip()
	text1.append(s)

text1 = filter(None, text1)	
#print(text1)

def findword(textlist, wordstring):
	try:
		lineno = -1
		for wordline in textlist:
			xx = wordline.split( )
			if ([w for w in xx if re.search(wordstring, w)]):
				lineno = textlist.index(wordline)
				textlist = textlist[lineno+1:]
				return textlist
			else:
				textlist = textlist[lineno+1:]
				return textlist
	except:
		pass

#-----------Read Database
with open('namedb.csv', 'rb') as f:
	reader = csv.reader(f)
	newlist = list(reader)    
newlist = sum(newlist, [])


def findname(textlist):
	lineno = -1
	try:
		for x in textlist:
			for y in x.split( ):
				if(difflib.get_close_matches(y.upper(), newlist)):
					lineno = text0.index(x)
					return lineno
				else:
					return lineno
	except:
		pass

# Searching for PAN
text0 = findword(text1, '(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$')
#print text0
	
panline = text0[0]
pan = panline.replace(" ", "")	
		

try:
	text0 = findword(text0, '(Name)$')
	print text0
	x = findname(text0)
	print x
	nameline1 = text0[x]
	text0 = text0[x+1:]
	text0 = findword(text0, '(Fathers Name|Father|Fathers|Father Name)$')
	x = findname(text0)
	nameline2 = text0[x]
	print nameline1
	print nameline2
except:
	pass


# Searching for Name and finding closest name in database
text0 = text0[namefine1()+1:]
print text0

try:
	for wordline in text0:
		xx = wordline.split( )
		if ([w for w in xx if re.search('(Fathers Name|Father|Fathers|Father Name)$', w)]):
			lineno = text0.index(wordline)
			break
	text0 = text0[lineno+1:]
except:
	pass
def namefine2():
	lineno = -1
	try:
		for x in text0:
			for y in x.split( ):
				if(difflib.get_close_matches(y.upper(), newlist)):
					nameline2 = x
					lineno = text0.index(x)
					return lineno
	except:
		pass

namefine2()
text0 = text0[namefine1()+1:]

try:
	name = nameline1
	print name
	fname = nameline2
	print fname
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
				break
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
