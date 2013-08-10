from base import BaseHandler
from resumeData import *
import datetime
import logging

class ResumeHandler(BaseHandler):
	def get(self):
		self.render("resume.html", 
			objective = ResumeManager().getObjective(),
			experienceList = ResumeManager().getExperienceList())

	def post(self):
		event = ResumeEvent(
			eventType = "Experience",
			company = "-",
			project = "-",
			startDate = datetime.date.today(),
			summary = "-")

		event.put()


class ResumeManager():
	def getObjective(self):
		return "Doing something awesome at a global scale"

	def getExperienceList(self):
		experienceList = []

		experienceList = ResumeEvent.all().order("-startDate").filter("eventType = ", "Experience")

		return experienceList
