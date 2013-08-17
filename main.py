import webapp2

from base import BaseHandler
from resume.resume import ResumeHandler
from blog.blog import BlogHandler

class MainHandler(BaseHandler):
	def get(self):
		self.render("main.html", css = "landing", title = "Hu Zhijia")

app = webapp2.WSGIApplication([	('/', MainHandler),
								('/blog', BlogHandler),
								('/resume', ResumeHandler)],
							   debug=True)

