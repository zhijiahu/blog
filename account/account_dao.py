from google.appengine.ext import db

class Account(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    salt = db.StringProperty(required=True)
    email = db.StringProperty()