:sparkles: This document for OCR :sparkles:

![PAN Card to JSON](PANOcr.jpg?raw=true "PAN Card image")

*****************************************************
Problem:
*****************************************************
	Extract information from image of Personal Account Number(PAN) Card
	by OCR in proper format[Standard according Indian Govt.].
		Imformation like - 
					Name, Father's Name, Date of Birth, PAN
*****************************************************



*****************************************************
Solution:
*****************************************************
	Steps:
		-> Take image
		-> crop to box(which has text in it)
		-> convert into gray scale(mono crome)
		-> give to tesseract
		-> text(output of tesseract)
	Now we will process this text means we will get meaningful information from it.
		-> find name using name database
		-> find father's name(assuming that second will be father's name)
		-> find year of birth
		-> find for PAN
*****************************************************


	
*****************************************************
Dependent packages
*****************************************************
	-python
	-opencv
	-numpy
	-pytesseract
	-JSON
	-difflib
	-csv
	-PIL
	-SciPy
	-dataparser
*****************************************************		



*****************************************************
Structure and Usage
*****************************************************
	Directories:
		src-
			which contains code files		
		testcases-
			which contains testing images
		result
			it contains JSON object
			
	Usage:
		python file_name.py [input image]
		Output will be JSON object name			 
	
*****************************************************
:point_left:
