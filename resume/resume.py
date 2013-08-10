from base import BaseHandler
from resumeData import *

class ResumeHandler(BaseHandler):
	def get(self):
		self.render("resume.html", 
			objective = ResumeManager().getObjective(),
			experienceList = ResumeManager().getExperienceList())

class ResumeManager():
	def getObjective(self):
		return "Doing something awesome at a global scale"

	def getExperienceList(self):
		experienceList = []

		ubisoftExperience = ResumeEvent(
			"Ubisoft Singapore",
			"Singapore", 
			"Programmer",
			datetime.date(2011,5,10), 
			None,
			['What did i do?', 'Something...'])

		experienceList.append(ubisoftExperience)

		return experienceList
