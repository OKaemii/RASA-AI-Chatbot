from glob import glob
import re
import os
import sys

import textract

from os import listdir
from os.path import isfile, join
mypath = r"files"

def bestFile(mypath, *argv):
	counter = 0
	max_val = 0
	best = ""
	
	for f in listdir(mypath):
		pthname = join(mypath, f)
		filetext = str(textract.process(pthname).decode("utf-8"))
		
		for word in argv:
			word = str(word.lower())
			instancesOWord = [m.start() for m in re.finditer(word, filetext)]
			counter += len(instancesOWord)
		
		if counter > max_val:
			best = f
			max_val = counter
	
	return best

def readLine(s):
	return s.split("\n")


#An algorithm that finds the most relevant keyword based on number of occurences
#then sorts which occurences are most relevant based on proximity of other key words
def relevanceRatio(text, *argv):
	rel = {} # relevance
	#text = text.lower()
	maxOccurrence = 0
	counter = 0

	#for every word's indexes, find every instance of word, and get its ratio to its closest keyword that we are searching
	#rank it by the totalling the ratios
	for w in argv:
		w = str(w.lower())
		instancesOWord = [m.start() for m in re.finditer(w, text)]
		if len(instancesOWord) > maxOccurrence:
			pivot = w
			counter += 1 
			maxOccurrence = len(instancesOWord)
		print('number of occurences of "' + w + '" in the text is', len(instancesOWord))

	print(pivot)
	arglist = list(argv)
	arglist.remove(pivot)

	instancesOKeyWord = [m.start() for m in re.finditer(pivot, text)]
	# for every index of word
	for wordIndex in instancesOKeyWord:
		# every instance of word will have a dictionary containing ratios from keywords, such that word:ratio
		rel[wordIndex] = {}
		# go through every keyword that we want to search in relation to it
		for keyword in arglist:
			# go through every instance of keyword in our text, and get its index
			keyIndexes = [m.start() for m in re.finditer(keyword, text)]
			# a ratio for every instance of keyword
			ratio = 0.0
			for keyIndex in keyIndexes:
				# find its ratio in relation to our word instance
				difference = wordIndex - keyIndex
				if (difference > 0):
					# if key is before word to search
					ratio = (difference)/wordIndex
				else:
					# if key is after word to search
					ratio = (-difference)/((len(text) - wordIndex))

				if (keyword in rel[wordIndex]):
					# if there exist a better ratio, use that
					if (ratio < rel[wordIndex][keyword]):
						rel[wordIndex][keyword] = ratio
				else:
					# initialise ratio
					rel[wordIndex][keyword] = ratio
					
					

	# make new dictionary with the sum of all ratios as new pair; key: sum(values)
	tempDict = {}
	for k, v in rel.items():
		tempDict[k] = sum(v.values())
	
	# sort the new dictionary by smallest ratio
	sortedRelRatio = {k: v for k, v in sorted(tempDict.items(), key=lambda item: item[1])}
	return sortedRelRatio


import bestFile2UseAlg as bf

#searches a given file and returns the first n most relevant occurrences based on the keywords provided
def searchfile(*argv):
    print(argv)
    # Find the most relevent file to use
    filename = bf.cosine_similarity(10, " ".join(argv))
    
    # If Fahad's code is unable to find a relevant file ..
    if filename is "":
        return "Sorry, I am not able to help! :( Please try rewording your query!"
    
    print("filename: {}".format(filename))
    text = textract.process(filename).decode("utf-8")
    text = str(text)
    
    # Calculate the relevance ratio
    rel = relevanceRatio(text.lower(), *argv)
    
    # Number of results to return.
    n = 1
    
    #label each occurence from 1 to n based on relevance using ratio algorithm
    for i in range(n):
        index = list(rel.keys())[i]
        text = text[:index] + " @" + str(i+1) + "@ " + text[index:]
    
    #print 5 lines above and 5 lines below the occurence
    searchlines = readLine(text)
    
    result = ""
    
    for position in range(1, n+1):
        for i, line in enumerate(searchlines):
            if ("@"+ str(position) + "@") in line.lower():
                searchlines[i] = searchlines[i].replace("@"+ str(position) + "@","")
                for l in searchlines[i-5:i+5]:
                    print(l,)
                    result = result + l + "\n"

    return result
