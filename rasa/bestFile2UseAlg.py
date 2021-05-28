from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

import os
import numpy as np
import math
import textract

import textract

# IMPORTANT - Required to make sure token, and stopwords work
#import nltk
#nltk.download('stopwords')
#nltk.download('punkt')

alpha = 0.3

# RESOURCE EXTRACTION

resourcePath = os.path.join(os.getcwd() + os.sep + os.pardir, "sean", "media", "resources")
# all folders in resource path
folders = [x[0] for x in os.walk(str(resourcePath))]

resourceLocations = [] 

unsupportedExtensions = [".py",".gz"]
# extract all resources within the root of resource path
for folder in folders:
	files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
	for file in files:
		resourceLocations.append(os.path.join(folder, file))

rescLength = len(resourceLocations)

# PREPROCESSING

def clearStopwords(dump):
	# init all stopwords
	stopWords = stopwords.words("english")
	words = word_tokenize(str(dump))

	# extracted text
	clean = ""

	# each word is not a stopword, nor empty string
	for word in words:
		if ((word not in stopWords) and (len(word) > 1)):
			clean = clean + " " + word

	return clean

def clearPunc(dump):
	symbols = "!,\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"

	for i in range(len(symbols)):
		dump = np.char.replace(dump, symbols[i], " ")

	# remove apostrophe(s)
	dump = np.char.replace(dump, "'", "")

	# remove trailing spaces
	dump = " ".join(str(dump).split())

	return dump

def stemming(dump):
	stemmer = PorterStemmer()

	tokens = word_tokenize(str(dump))

	clean = ""
	for word in tokens:
		clean = clean + " " + stemmer.stem(word)

	return clean

def preprocess(data):
	# bring data to lowercase
	data = np.char.lower(data)
	
	# clean data for removal of stopwords
	data = clearPunc(data)
	# get rid of useless words
	data = clearStopwords(data)
	# get rid of any other punctuation
	data = clearPunc(data)

	data = stemming(data)

	return data


# EXTRACTING DATA

processedData = []

for file in resourceLocations:
	data = str(textract.process(file).strip())
	processedData.append(word_tokenize(str(preprocess(data))))

# CALCULATE DF FOR ALL WORDS

docFreq = {}

for index in range(rescLength):
	tokens = processedData[index]
	for word in tokens:
		try:
			docFreq[word].add(index)
		except:
			docFreq[word] = {index}

	tokens = processedData[index]
	for word in tokens:
		try:
			docFreq[word].add(index)
		except:
			docFreq[word] = {index}
for index in docFreq:
	docFreq[index] = len(docFreq[index])


totalVocabSize = len(docFreq)
totalVocab = [vocab for vocab in docFreq]

def doc_freq(word):
	char = 0
	try:
		char = docFreq[word]
	except:
		pass
	return char

# Calculating TF-IDF for body

doc = 0
tfIdf = {}

for index in range(rescLength):
	tokens = processedData[index]

	counter = Counter(tokens + processedData[index])
	wordsCount = len(tokens + processedData[index])

	for token in np.unique(tokens):
		tf = counter[token] / wordsCount
		df = doc_freq(token)
		idf = np.log((rescLength + 1)/(df + 1))

		tfIdf[doc, token] = tf * idf

	doc += 1

# Calculating TF-IDF for title

doc = 0
tfIdfTitle = {}

for index in range(rescLength):
	
	tokens = processedData[index]
	counter = Counter(tokens + processedData[index])
	wordsCount = len(tokens + processedData[index])

	for token in np.unique(tokens):
		
		tf = counter[token]/wordsCount
		df = doc_freq(token)

		# 1 is added to avoid negatives
		idf = np.log((rescLength + 1)/(df + 1))
		
		tfIdfTitle[doc, token] = tf * idf

	doc += 1


# Merging TF-IDF ACCORDING TO WEIGHTS

for index in tfIdf:
	tfIdf[index] *= alpha

for index in tfIdfTitle:
	tfIdf[index] = tfIdfTitle[index]


# RANKINGS

# TF-IDF Cosine Similarity

# cosine similarity
def cosine_sim(a, b):
	cosSim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
	return cosSim

# Vectorising tf-idf

D = np.zeros((rescLength, totalVocabSize))
for index in tfIdf:
	try:
		ind = totalVocab.index(index[1])
		D[index[0]][ind] = tfIdf[index]
	except:
		pass


def gen_vector(tokens):

	Q = np.zeros((len(totalVocab)))
	
	counter = Counter(tokens)
	wordsCount = len(tokens)
	
	for token in np.unique(tokens):
		
		tf = counter[token]/wordsCount
		df = doc_freq(token)
		idf = math.log((rescLength+1)/(df+1))

		try:
			ind = totalVocab.index(token)
			Q[ind] = tf*idf
		except:
			pass
	return Q

def cosine_similarity(matchScore, query):
	preprocessed_query = preprocess(query)
	tokens = word_tokenize(str(preprocessed_query))
	
	print("\nQuery: ", query)
	print("Tokens: ",tokens)
	print("Path: ", resourcePath)
	print("Documents: ", len(D))
	
	dCosines = []
	
	queryVector = gen_vector(tokens)
	
	for d in D:
		dCosines.append(cosine_sim(queryVector, d))
		
	matches = np.array(dCosines).argsort()[-matchScore:][::-1]
	
	# if no files were found
	if (len(matches) <= 1):
		return ""
	
	# return first best match
	print("\n","using: ",resourceLocations[matches[0]], "\n")
	return resourceLocations[matches[0]]

# TOKEN ID TO DOC

def print_doc(id):
	text = str(textract.process(resourceLocations[id]))
	return text


def retResLoc():
	return resourceLocations


#print(Q)
#print_doc(Q[0])
