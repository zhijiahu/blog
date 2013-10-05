from base import BaseHandler

class ProjectsHandler(BaseHandler):
	def get(self):
		self.render("projects.html")

	def post(self):
		pass
