import datetime

class Resume():
	def __init__(self, objective, experienceList, skillsList, projectList, educationList, interests):
		self.objective = objective
		self.experienceList = experienceList
		self.skillsList = skillsList
		self.projectList = projectList
		self.educationList = educationList
		self.interests = interests

class ResumeEvent():
	def __init__(self, company, location, jobTitle, startDate, endDate, summaryList):
		self.company = company
		self.location = location
		self.jobTitle = jobTitle
		self.startDate = startDate
		self.startDateText = startDate.strftime("%B %Y")
		if not endDate:
			self.endDate = datetime.date.today()
			self.endDateText = "Present"
		else:
			self.endDate = endDate
			self.endDateText = endDate.strftime("%B %Y")
		self.summaryList = summaryList