import unittest
import os

from ..python import BestFile2UseAlg

class TestBestFile2UseAlg(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.bestfile = BestFile2UseAlg.BestFile2UseAlg()

	def testClearStopwordsStopword(self):
		result = self.bestfile.clearStopwords("the no can")
		control = ""
		self.assertEqual(control, result)

	def testClearStopwordsWord(self):
		test = "word test happy"
		result = self.bestfile.clearStopwords(test)
		control = " word test happy"
		self.assertEqual(control, result)

	def testClearStopwords(self):
		result = self.bestfile.clearStopwords("word and yes, no can do")
		control = "word yes"
		self.assertIn(control, result)

	def testclearPuncPunc(self):
		test = "!,#$%&()*+-./:;<=>?@[\]^_`{|}~  '' ``"
		result = self.bestfile.clearPunc(test)
		control = ""
		self.assertEqual(control, result)

	def testclearPuncWord(self):
		test = "word test happy"
		result = self.bestfile.clearPunc(test)
		self.assertEqual(test, result)

	def testclearPunc(self):
		result = self.bestfile.clearPunc("word! and@@ yes, no 'can;'][] do")
		control = "word and yes no can do"
		self.assertIn(control, result)

	def testCosineSimilarityEasy(self):
		result = self.bestfile.cosine_similarity(10, "<test!>Hello World<Test!>")
		control = "test.txt"
		self.assertIn(control, result)

	def testCosineSimilarityMedium(self):
		result = self.bestfile.cosine_similarity(10, "A DBMS combines all the functions of data storage and access for a related set of tasks")
		control = "pdfToStrTestFile"
		self.assertIn(control, result)

	def testCosineSimilarityHard(self):
		result = self.bestfile.cosine_similarity(10, "Courses will be taught over ten weeks.")
		control = "SPP"
		self.assertIn(control, result)


if __name__ == '__main__':
	unittest.main()