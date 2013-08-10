import webapp2

from resume.resume import ResumeHandler

app = webapp2.WSGIApplication([('/resume', ResumeHandler)],
							   debug=True)
