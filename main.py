import webapp2

from base import BaseHandler
from resume.resume import ResumeHandler
from blog.blog import *
from account.account import *
from projects.projects import *

class MainHandler(BaseHandler):
	def get(self):
		self.render("main.html", css = "landing", title = "Hu Zhijia", hostname = self.request.host)

app = webapp2.WSGIApplication([	('/', MainHandler),
								('/signup', SignupHandler),
								('/login', LoginHandler),
							   	('/logout', LogoutHandler),
								('/blog/?', BlogViewAllHandler),
							   	('/blog/.json', BlogViewAllJsonHandler),
							   	('/blog/([0-9]+)', BlogViewByIdHandler),
							   	('/blog/([0-9]+.json)', BlogViewByIdJsonHandler),
							   	('/blog/newpost', BlogNewHandler),
							   	('/blog/edit/([0-9]+)', BlogEditHandler),
							   	('/blog/edit', BlogEditHandler),
							   	('/blog/flush', BlogFlushHandler),
								('/resume', ResumeHandler),
								('/projects', ProjectsHandler)],
							   debug=True)

