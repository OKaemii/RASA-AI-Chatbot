from glob import glob
import re
import os
import sys

import win32com.client as win32
import textract
from win32com.client import constants



def docToDocx(path):
    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)
    
def readLine(s):
    return s.split("\n")

def relevanceRatio(text, *argv):
    rel = {} # relevance
    text = text.lower()
    maxOccurrence = 0
    counter = 0
    #instancesOfword = a list of every word's index in text
    #keyWords = a list of every index of keyword in text
    #rel = a dictionary of every keyword, and their distance to word as a ratio
    
    #for every word's indexes, find every instance of word, and get its ratio to its closest keyword that we are searching
    #rank it by the totalling the ratios
    for w in argv:
        w = w.lower()
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

def searchfile(text, n=1):
    rel = relevanceRatio(text.lower(), "degree", "honours", "social & public policy")
    i = 0
    
    '''while i < 3:
        index = list(rel.keys())[i]
        print(text[index-100:index +100])
        print("\n\n\n")
        i += 1'''
    
    #could change to for loop
    for i in range(n):
        index = list(rel.keys())[i]
        text = text[:index] + " @" + str(i+1) + "@ " + text[index:]
    #print(index)
    
    
        
    searchlines = readLine(text)
    for position in range(1,n+1):
        for i, line in enumerate(searchlines):
            if ("@"+ str(position) + "@") in line.lower():
                searchlines[i] = searchlines[i].replace("@"+ str(position) + "@","")
                for l in searchlines[i-5:i+5]:
                    print(l,)
                print("\n\n")

    #for i, line in enumerate(searchlines):
    #    if word.lower() in line.lower():
    #        for l in searchlines[i-n:i+n]:
    #            print(l,)
    #        print("\n\n")

file = "SPP"
path = ""
#docToDocx(path + file + ".pdf")
text = textract.process(path + file + ".docx")
#print(text, type(text))
searchfile(text.decode("utf-8"), 3)