# -*- coding: utf-8 -*-

from base import BaseHandler
from resumeData import *
import datetime
import logging

class ResumeHandler(BaseHandler):
	def get(self):
		self.render("resume.html", 
			title = u"Hu Zhijia - Résumé",
			objective = ResumeManager().getObjective(),
			experienceList = ResumeManager().getEventList("Experience"),
			skillsList = ResumeManager().getThingList("Skills"),
			projectList = ResumeManager().getEventList("Projects"),
			educationList = ResumeManager().getEventList("Education"),
			interestList = ResumeManager().getThingList("Interests"))

	def post(self):
		event = ResumeEvent(
			eventType = "Experience",
			eventName = "-",
			organization = "-",
			startDate = datetime.date.today(),
			endDate = datetime.date.today(),
			summary = "-\n-")

		event.put()

		thing = ResumeThing(
			thingType = "-",
			summary = "-")
		thing.put()


class ResumeManager():
	def getObjective(self):
		objective = ResumeThing.all().filter("thingType = ", "Objective").get()

		if objective:
			return objective.summary

		return "Doing something awesome"

	def getEventList(self, eventType):
		eventList = []

		eventList = ResumeEvent.all().order("-startDate").filter("eventType = ", eventType)

		return eventList

	def getThingList(self, thingType):
		thingList = []

		thingList = ResumeThing.all().filter("thingType = ", thingType)

		return thingList
