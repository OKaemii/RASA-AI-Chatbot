import unittest
import os
import textract

from ..python import RefactoredSearch

class TestRefactoredSearch(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.refsearch = RefactoredSearch.RefactoredSearch()

	testFilePath = os.path.join(os.path.dirname(__file__), "resources/pdfToStrTestFile.pdf")
	text = textract.process(testFilePath).decode("utf-8")
	
	def testRelevanceRatioSimilarDBS(self):
		result = self.refsearch.relevanceRatio(self.text, "Avoiding Redundancy","Ambiguity","Inconsistency","Wasted Effort","Redundancy", "Effort")
		control = 1650
		self.assertEqual(control, list(result.keys())[0])

	def testRelevanceRatioSimilarDBS2(self):
		testFilePath = os.path.join(os.path.dirname(__file__), "resources/pdfToStrTestFile.pdf")
		text = textract.process(testFilePath).decode("utf-8")

		result = self.refsearch.relevanceRatio(self.text, "Website Designers","designs","interface","extended functionality","Database")
		control = 3697
		self.assertEqual(control, list(result.keys())[0])

	def testRelevanceRatioSimilarDBS3(self):
		result = self.refsearch.relevanceRatio(self.text, "degree","cardinality","Cardinality of a Relation")
		control = 11534
		self.assertEqual(control, list(result.keys())[0])

	def testSearchFileSTest(self):
		result = self.refsearch.searchFile("Hello","World")
		control = "Hello World"
		self.assertIn(control, result)

	def testSearchFileSPP(self):
		result = self.refsearch.searchFile("ACTIVE CITIZENSHIP","Course","Credits")
		control = "80"
		self.assertIn(control, result)

	def testSearchFileSPP2(self):
		result = self.refsearch.searchFile("Course content","examines","course", "responses ")
		control = "course examines the growth of cities"
		self.assertIn(control, result)

	def testSearchFileSPP3(self):
		result = self.refsearch.searchFile("QUALITATIVE METHODS","compulsory","Junior", "Honours")
		control = "Each course module is worth 20 credits"
		self.assertIn(control, result)

	def testSearchFileDBM(self):
		result = self.refsearch.searchFile("DBMS","Management","System", "functions", "data", "storage")
		control = "DBMS combines all the functions of data storage and access for a related set of tasks"
		self.assertIn(control, result)

	def testSearchFileDBM2(self):
		result = self.refsearch.searchFile("database","Management","System", "functions", "data", "storage")
		control = "DBMS combines all the functions of data storage and access for a related set of tasks"
		self.assertIn(control, result)

	def testSearchFileDBM3(self):
		result = self.refsearch.searchFile("Schema","tuple","relation", "attributes")
		control = "is a row of a relation"
		self.assertIn(control, result)

if __name__ == '__main__':
	unittest.main()