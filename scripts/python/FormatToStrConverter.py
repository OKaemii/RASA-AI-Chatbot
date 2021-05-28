import textract

# Author: 2327846P - Veronika A. Polakova
# Action: Converts the format of (close to any) file to str and returns it.
class FormatToStrConverter:

	def formatToStr(self, filename):
		txt = textract.process(filename)
		txt = str(txt, 'utf-8')
		# optionally remove newlines
		# txt = txt.replace("\n", " ")
		return txt