import unittest
import os

from ..python import FormatToStrConverter

class TestFormatToStrConverter(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.formatConverter = FormatToStrConverter.FormatToStrConverter()

	def testFormatToStrPDF(self):
		testFilePath = os.path.join(os.path.dirname(__file__), "resources/pdfToStrTestFile.pdf")
		readTxt = self.formatConverter.formatToStr(testFilePath)
		control = "Data storage tool must provide the following features"
		self.assertIn(control, readTxt)

	def testFormatToStrTXT(self):
		testFilePath = os.path.join(os.path.dirname(__file__), "resources/test.txt")
		readTxt = self.formatConverter.formatToStr(testFilePath)
		control = "<test!>Hello World<Test!>"
		self.assertEqual(control, readTxt)
	
	def testFormatToStrDOCX(self):
		testFilePath = os.path.join(os.path.dirname(__file__), "resources/SPP.docx")
		readTxt = self.formatConverter.formatToStr(testFilePath)
		control = "Develop an awareness of the concepts of health and health inequalities"
		self.assertIn(control, readTxt)	


if __name__ == '__main__':
	unittest.main()