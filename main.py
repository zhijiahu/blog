import webapp2

from base import BaseHandler
from resume.resume import ResumeHandler

class MainHandler(BaseHandler):
	def get(self):
		self.render("main.html")

app = webapp2.WSGIApplication([	('/', MainHandler),
								('/resume', ResumeHandler)],
							   debug=True)

