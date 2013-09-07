from base import BaseHandler

from google.appengine.ext import db
import json
from google.appengine.api import memcache
import time
import logging

FRONT_PAGE_CACHE = "front_page"
LAST_QUERIED_CACHE = "last_queried"

class BlogViewByIdHandler(BaseHandler):
	def get(self, article_id):
			last_queried, postById = Article.get_post_by_id(int(article_id))
			posts = [postById]
			secs_ago = int(time.time() - last_queried)
			self.render("blog.html", blog = True, posts = posts, secs_ago = secs_ago)

	def post(self):
		self.redirect("/blog/newpost")

class BlogViewByIdJsonHandler(BaseHandler):
	def get(self, article_id_json):
		article_id = article_id_json[:-5]
		last_queried, postById = Article.get_post_by_id(int(article_id))
		self.response.headers['Content-Type'] = 'application/json'
		self.write(json.dumps(postById.to_dict()))


class BlogViewAllHandler(BaseHandler):
	def get(self):
		#blogs = db.GqlQuery("SELECT * FROM Article ORDER BY created DESC")
		last_queried, posts = Article.get_all_posts()

		secs_ago = int(time.time() - last_queried)
		self.render("blog.html", blog = True, posts = posts, secs_ago = secs_ago)

	def post(self):
		self.redirect("/blog/newpost")

class BlogViewAllJsonHandler(BaseHandler):
	def get(self):
		last_queried, posts = Article.get_all_posts()
		self.response.headers['Content-Type'] = 'application/json'
		self.write(json.dumps(list(x.to_dict() for x in posts)))


class Article(db.Model, BaseHandler):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	lang = db.StringProperty()

	@staticmethod
	def get_all_posts():
		posts = memcache.get(FRONT_PAGE_CACHE)

		if posts:
			return memcache.get(LAST_QUERIED_CACHE), posts

		posts = Article.all().order("-created")
		logging.info("DB query all")
		timenow = time.time();
		memcache.set(LAST_QUERIED_CACHE, timenow)
		memcache.set(FRONT_PAGE_CACHE, posts)

		return timenow, posts

	@staticmethod
	def get_post_by_id(id):
		cache_key_post = FRONT_PAGE_CACHE + str(id)
		cache_key_last_queried = LAST_QUERIED_CACHE + str(id)

		post = memcache.get(cache_key_post)

		if post:
			return memcache.get(cache_key_last_queried), post

		post = Article.get_by_id(id)
		logging.info("DB query single")
		timenow = time.time()
		memcache.set(cache_key_last_queried, timenow)
		memcache.set(cache_key_post, post)

		return timenow, post

	def render(self):
		return self.render_str("post.html", p = self)

	def to_dict(self):
		return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class BlogFlushHandler(BaseHandler):
	def get(self):
		memcache.flush_all()
		self.redirect("/blog")

class BlogNewHandler(BaseHandler):
	def get(self):
		if self.isSuperman():
			self.render("newpost.html", blog = True)
		else:
			self.redirect("/login")

class BlogEditHandler(BaseHandler):
	def get(self,article_id):
		last_queried, postById = Article.get_post_by_id(int(article_id))
	
		params = dict(	subject = postById.subject,
						content = postById.content,
						lang = postById.lang,
						article_id = article_id,
						blog = True)

		self.render("newpost.html", **params)

	def post(self):
		article_id = self.request.get("article_id")
		subject = self.request.get("subject")
		content = self.request.get("content")
		lang = self.request.get("lang")

		params = dict(	subject = subject,
						content = content,
						blog = True)

		haveError = False

		# Validation
		if not subject:
			params["error_subject"] = "*"
			haveError = True

		if not content:
			params["error_content"] = "*"
			haveError = True

		if haveError:
			self.render("newpost.html", **params)
		else:
			if article_id:
				last_queried, postById = Article.get_post_by_id(int(article_id))
				postById.subject = subject
				postById.content = content
				postById.lang = lang
				postById.put()
			else:
				newArticle = Article(subject = subject, content = content, lang = lang)
				newArticle.put()
				article_id = newArticle.key().id()

			memcache.flush_all()
			self.redirect("/blog/" + str(article_id))





	
