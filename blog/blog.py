from base import BaseHandler

class BlogHandler(BaseHandler):
	def get(self):
		self.render("blog.html", css = "blog")