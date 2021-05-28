import unittest
from ..python import WebpageHandler

class TestWebpageHandler(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.wpHandler = WebpageHandler.WebpageHandler()

	def testReadWebpage_writingStudyAdvice(self):
		readTxt = self.wpHandler.readWebpage("https://www.gla.ac.uk/myglasgow/leads/students/writingstudyadvice/socialsciences/")
		control = "Students in Social Sciences can make an appointment or come to a class with the Effective Learning Adviser for the College (or her Graduate Teaching Assistants) to talk about anything related to their academic work. Common topics include:"
		readTxt = readTxt.replace("\n", " ")
		self.assertIn(control, readTxt)

	def testReadWebpage_assessmentFeedbackToolkit(self):
		readTxt = self.wpHandler.readWebpage("https://www.gla.ac.uk/myglasgow/leads/aftoolkit/studentinfo/")
		control = "The Assessment and Feedback Toolkit was designed with both staff and students in mind, so you can explore the whole Toolkit. You will also find links to further reading materials and relevant resources, where appropriate."
		readTxt = readTxt.replace("\n", " ")
		self.assertIn(control, readTxt)

	def testHtmlToStr_writingStudyAdvice(self):
		htmlTest = "columns content eight large-8 medium-8 '><h2 class='unresponsivestyle'>Academic Advice in Social Sciences</h2><p>Students in Social Sciences can make an appointment or come to a class with the Effective Learning Adviser for the College (or her Graduate Teaching Assistants) to talk about anything related to their academic work. Common topics include:</p><ul class='date_change_pair'><ul>"
		htmlTxt = self.wpHandler.htmlToStr(htmlTest)
		htmlTxt = htmlTxt.replace("\n", " ")
		control = "Students in Social Sciences can make an appointment or come to a class with the Effective Learning Adviser for the College (or her Graduate Teaching Assistants) to talk about anything related to their academic work. Common topics include:"
		self.assertIn(control, htmlTxt)

	def testHtmlToStr_assessmentFeedbackToolkit(self):
		htmlTest = "<p>In addition to these, there is a separate <a href='/myglasgow/leads/aftoolkit/resources/students/'>student resources</a> section, where you can find tools to help you with assessment and feedback.</p><p>The Assessment and Feedback Toolkit was designed with both staff and students in mind, so you can explore the whole Toolkit. You will also find links to further reading materials and relevant resources, where appropriate.&nbsp;</p>"
		htmlTxt = self.wpHandler.htmlToStr(htmlTest)
		htmlTxt = htmlTxt.replace("\n", " ")
		control = "The Assessment and Feedback Toolkit was designed with both staff and students in mind, so you can explore the whole Toolkit. You will also find links to further reading materials and relevant resources, where appropriate."
		self.assertIn(control, htmlTxt)


if __name__ == '__main__':
	unittest.main()