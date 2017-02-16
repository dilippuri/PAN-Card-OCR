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
import subprocess
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

subprocess.call("tesseract "+path+" out -4", shell=True)
fi = open('out.txt', 'r')
text = fi.read()
#text = pytesseract.image_to_string(Image.open('temp.jpg'))
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
#print "++++++++++++++++++++++++++++++++++++"
def findword(textlist, wordstring):
	lineno = -1
	for wordline in textlist:
		xx = wordline.split( )
		if ([w for w in xx if re.search(wordstring, w)]):
			lineno = textlist.index(wordline)
			textlist = textlist[lineno+1:]
			return textlist
	return textlist

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
				print y
				if(difflib.get_close_matches(y.upper(), newlist)):
					lineno = textlist.index(x)
					return lineno
		return lineno
	except:
		pass

# Searching for PAN
text0 = findword(text1, '(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$')
panline = text0[0]
pan = panline.replace(" ", "")	

# Searching for NAME
try:
	word1 = '(/NAME|/Name|NAME|Name)$'
	text0 = findword(text0, word1)
	nameline1 = text0[0]
	text0 = text0[1:]
	word2 = '(/FATHERS| NAME|/FATHERS NAME|/FATHER S NAME|/FATHER NAME|/FATHER|/Fathers Name|/Father|/Fathers|/Father Name|FATHERS NAME|FATHER S NAME|FATHER NAME|FATHER|Fathers Name|Father|Fathers|Father Name)$'
	text0 = findword(text0, word2)
	nameline2 = text0[0]
	text0 = text0[1:]
except:
	pass


# Searching for Name and finding closest name in database
try:
	name = nameline1
	fname = nameline2
except:
	pass

try:
	word3 = '(/DATE|BIRTH|/DATE OF BIRTH|DATE|DATE OF BIRTH|Date)$'
	text0 = findword(text0, word3)
	dobline = text0[0]
	text0 = text0[1:]
#	print dobline
	if(dparser.parse(dobline, fuzzy=True)):
		dob = dparser.parse(dobline,fuzzy=True).year
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
'''
print "+++++++++++++++++++++++++++++++"     
print(data['Name'])
print "-------------------------------"
print(data['Father Name'])
print "-------------------------------"
print(data['Date of Birth'])
print "-------------------------------"
print(data['PAN'])
print "-------------------------------"
#'''
