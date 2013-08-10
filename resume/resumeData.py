import datetime
from google.appengine.ext import db

class ResumeEvent(db.Model):
	eventType = db.StringProperty(required = True)
	company = db.StringProperty(required = True)
	location = db.StringProperty(default = "Singapore")
	project = db.StringProperty(required = True)
	role = db.StringProperty(default = "Programmer")
	startDate = db.DateProperty(required = True)
	endDate = db.DateProperty()
	summary = db.TextProperty(required = True)