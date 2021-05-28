import urllib.request
import html2text

# Author: 2327846P - Veronika A. Polakova
# Action: Accesses and returns as str webpage text.
class WebpageHandler:

	def readWebpage(self, urlString):
		page = urllib.request.urlopen(urlString)
		pageHtml = page.read()
		pageTxt = self.htmlToStr(pageHtml)
		return pageTxt

	def htmlToStr(self, pageHtml):
		htmlHandler = html2text.HTML2Text()
		# If set to False, the link reference will appear
		htmlHandler.ignore_links = True
		if not isinstance(pageHtml, str):
			pageHtml = str(pageHtml, 'utf-8')
		txt = htmlHandler.handle(pageHtml)
		return txt