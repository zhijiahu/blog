import webapp2

from base import BaseHandler
from resume.resume import ResumeHandler
from blog.blog import BlogViewAllHandler, BlogViewByIdHandler, BlogNewHandler, BlogViewAllJsonHandler, BlogViewByIdJsonHandler, BlogFlushHandler

class MainHandler(BaseHandler):
	def get(self):
		self.render("main.html", css = "landing", title = "Hu Zhijia")

app = webapp2.WSGIApplication([	('/', MainHandler),
								('/blog/?', BlogViewAllHandler),
							   	('/blog/.json', BlogViewAllJsonHandler),
							   	('/blog/([0-9]+)', BlogViewByIdHandler),
							   	('/blog/([0-9]+.json)', BlogViewByIdJsonHandler),
							   	('/blog/newpost', BlogNewHandler),
							   	('/blog/flush', BlogFlushHandler),
								('/resume', ResumeHandler)],
							   debug=True)

