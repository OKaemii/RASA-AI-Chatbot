from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

import re, string, os
import numpy as np
import math
import textract

class BestFile2UseAlg:
    alpha = 0.3
    resourceLocations = [] 
    rescLength = 0

    docFreq = {}
    totalVocabSize = 0
    totalVocab = []

    tfIdf = {}
    tfIdfTitle = {}

    D = np.zeros((0,0))

    def __init__(self):
        nltk.download("stopwords")
        nltk.download("punkt")
        # RESOURCE EXTRACTION
        resourcePath = os.path.join(os.getcwd() + os.sep, "scripts", "tests", "resources")
        # all folders in resource path
        folders = [x[0] for x in os.walk(str(resourcePath))]

        # extract all resources within the root of resource path
        for folder in folders:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
            for file in files:
                self.resourceLocations.append(os.path.join(folder, file))
        self.rescLength = len(self.resourceLocations)
        # PREPROCESSING and EXTRACTING DATA
        processedData = self.extractingData()

        # Calculate DF for all words using pre processed data
        self.calculateDfForAllWords(processedData)

        # Calculate Tf-Idf for content of file
        self.calculateTfIdfForAllBody(processedData, self.rescLength)
        # Calculate Tf-Idf for title of file
        self.calculateTfIdfForAllTitle(processedData, self.rescLength)

        # Merging TF-IDF ACCORDING TO WEIGHTS
        for index in self.tfIdf:
            self.tfIdf[index] *= self.alpha
        for index in self.tfIdfTitle:
            self.tfIdf[index] = self.tfIdfTitle[index]

        # Vectorising tf-idf

        D = np.zeros((self.rescLength, self.totalVocabSize))
        self.D = self.vectoriseTfIdf(D)


    def clearStopwords(self,dump):
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

    def clearPunc(self, dump):
        symbols = "!,\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"

        for i in range(len(symbols)):
            dump = np.char.replace(dump, symbols[i], " ")

        # remove apostrophe(s)
        dump = np.char.replace(dump, "'", "")

        # remove trailing spaces
        dump = " ".join(str(dump).split())

        return dump

    def stemming(self, dump):
        stemmer = PorterStemmer()

        tokens = word_tokenize(str(dump))

        clean = ""
        for word in tokens:
            clean = clean + " " + stemmer.stem(word)

        return clean

    def preprocess(self, data):
        # bring data to lowercase
        data = np.char.lower(data)
        
        # clean data for removal of stopwords
        data = self.clearPunc(data)
        # get rid of useless words
        data = self.clearStopwords(data)
        # get rid of any other punctuation
        data = self.clearPunc(data)

        data = self.stemming(data)

        return data

    # EXTRACTING DATA
    def extractingData(self):
        processedData = []

        for file in self.resourceLocations:
            data = str(textract.process(file).strip())
            processedData.append(word_tokenize(str(self.preprocess(data))))
        return processedData

    # CALCULATE DF FOR ALL WORDS
    def calculateDfForAllWords(self, processedData):
        for index in range(self.rescLength):
            tokens = processedData[index]
            for word in tokens:
                try:
                    self.docFreq[word].add(index)
                except:
                    self.docFreq[word] = {index}

            tokens = processedData[index]
            for word in tokens:
                try:
                    self.docFreq[word].add(index)
                except:
                    self.docFreq[word] = {index}
        for index in self.docFreq:
            self.docFreq[index] = len(self.docFreq[index])

        self.totalVocabSize = len(self.docFreq)
        self.totalVocab = [vocab for vocab in self.docFreq]

    def doc_freq(self, word):
        char = 0
        try:
            char = self.docFreq[word]
        except:
            pass
        return char

    # Calculating TF-IDF for body
    def calculateTfIdfForAllBody(self, processedData, rescLength):
        doc = 0

        for index in range(rescLength):
            tokens = processedData[index]
            counter = Counter(tokens + processedData[index])
            wordsCount = len(tokens + processedData[index])

            for token in np.unique(tokens):
                tf = counter[token] / wordsCount
                df = self.doc_freq(token)
                idf = np.log((rescLength + 1)/(df + 1))

                self.tfIdf[doc, token] = tf * idf
            doc += 1

    # Calculating TF-IDF for title
    def calculateTfIdfForAllTitle(self, processedData, rescLength):
        doc = 0

        for index in range(rescLength):
            tokens = processedData[index]
            counter = Counter(tokens + processedData[index])
            wordsCount = len(tokens + processedData[index])

            for token in np.unique(tokens):
                tf = counter[token]/wordsCount
                df = self.doc_freq(token)

                # 1 is added to avoid negatives
                idf = np.log((rescLength + 1)/(df + 1))
                
                self.tfIdfTitle[doc, token] = tf * idf
            doc += 1


    # RANKINGS

    # TF-IDF Cosine Similarity

    # cosine similarity
    def cosine_sim(self, a, b):
        cosSim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
        return cosSim

    # Vectorising tf-idf
    def vectoriseTfIdf(self, D):
        for index in self.tfIdf:
            try:
                ind = self.totalVocab.index(index[1])
                D[index[0]][ind] = self.tfIdf[index]
            except:
                pass
        return D

    def genVector(self, tokens):
        Q = np.zeros((len(self.totalVocab)))
        
        counter = Counter(tokens)
        wordsCount = len(tokens)
        
        for token in np.unique(tokens):
            
            tf = counter[token]/wordsCount
            df = self.doc_freq(token)
            idf = math.log((self.rescLength+1)/(df+1))

            try:
                ind = self.totalVocab.index(token)
                Q[ind] = tf*idf
            except:
                pass
        return Q

    def cosine_similarity(self, matchScore, query):
        preprocessed_query = self.preprocess(query)
        tokens = word_tokenize(str(preprocessed_query))

        dCosines = []
        
        queryVector = self.genVector(tokens)
            
        for d in self.D:
            dCosines.append(self.cosine_sim(queryVector, d))
            
        matches = np.array(dCosines).argsort()[-matchScore:][::-1]
        # if no files were found
        if (len(matches) <= 1):
            return ""
        
        # return first best match
        # return matches[0] # <-- this should be used
        return self.resourceLocations[matches[0]] # <-- using this as a bodge

    # TOKEN ID TO DOC

    def print_doc(self, id):
        text = str(textract.process(resourceLocations[id]))
        return text

    def retResLoc(self):
        return resourceLocations