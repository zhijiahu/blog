import datetime
from google.appengine.ext import db

class ResumeEvent(db.Model):
	eventType = db.StringProperty(required = True)
	eventName = db.StringProperty(required = True)
	organization = db.StringProperty(required = True)
	location = db.StringProperty()
	role = db.StringProperty(default = "Programmer")
	startDate = db.DateProperty(required = True)
	endDate = db.DateProperty()
	summary = db.StringProperty(multiline=True)

class ResumeThing(db.Model):
	thingType = db.StringProperty(required = True)
	summary = db.StringProperty(required = True)