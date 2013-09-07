import webapp2
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class BaseHandler(webapp2.RequestHandler):
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		if self.isSuperman():
			kw["superman"] = 'hacker'
		self.response.write(self.render_str(template, **kw))

	def write(self, _str):
		self.response.write(_str)

	def set_user_cookie(self, username):
		secure_user_cookie = self.make_secure_val(username)
		self.response.headers.add_header('Set-Cookie', str('user=%s; Path=/' % secure_user_cookie))

	def clear_user_cookie(self):
		self.response.headers.add_header('Set-Cookie', str('user=; Path=/'))

	def isSuperman(self):
		user_cookie = self.request.cookies.get('user')

		if user_cookie:
			return user_cookie.split("|")[0] == 'zhijia'
		else:
			return None