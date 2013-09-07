import re
import string
import random
import hmac
import hashlib
from base import BaseHandler
from google.appengine.ext import db

SECRET = 'youdontknowwhatisthis'

class Account(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    salt = db.StringProperty(required=True)
    email = db.StringProperty()


class AccountHandler(BaseHandler):
    def __make_salt(self):
        return ''.join(random.choice(string.letters) for _ in xrange(5))

    def make_pw_hash(self, name, pw, salt=None):
        if not salt:
            salt = self.__make_salt()

        h = hashlib.sha256(name + pw + salt).hexdigest()
        return [h, salt]

    def hash_str(self, s):
        return hmac.new(SECRET,s).hexdigest()

    def make_secure_val(self, s):
        return "%s|%s" % (s, self.hash_str(s))

    def check_secure_val(self, h):
        val = h.split('|')[0]
        if h == self.make_secure_val(val):
            return val

class SignupHandler(AccountHandler):
    def get(self):
        self.writeSignupForm()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_errorMsg = ""
        password_errorMsg = ""
        verify_errorMsg = ""
        email_errorMsg = ""

        db_users = Account.all()
        db_users.filter("username =", username)
        user_account = db_users.get()

        if user_account:
            username_errorMsg = "User already exists."

        if not self.validateUserName(username):
            username_errorMsg = "That's not a valid username."

        if not self.validatePassword(password):
            password_errorMsg = "That wasn't a valid password."

        elif password != verify:
            verify_errorMsg = "Your passwords didn't match."

        if not self.validateEmail(email):
            email_errorMsg = "That's not a valid email."

        if username_errorMsg or password_errorMsg or verify_errorMsg or email_errorMsg:
            self.writeSignupForm(username, email, username_errorMsg, password_errorMsg, verify_errorMsg, email_errorMsg)
        else:
            # Create new user in database
            secure_pw = self.make_pw_hash(username, password)
            new_user = Account(username = username, password = secure_pw[0], salt = secure_pw[1], email = email)
            new_user.put()

            self.set_user_cookie(username)

            self.redirect("/blog")


    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    def validateUserName(self, username):
        return username and self.USER_RE.match(username)        

    PASSWORD_RE = re.compile(r"^.{3,20}$")
    def validatePassword(self, password):
        return password and self.PASSWORD_RE.match(password)

    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    def validateEmail(self, email):
        return not email or self.EMAIL_RE.match(email)


    def writeSignupForm(self, username = "", email = "", username_errorMsg = "", password_errorMsg = "", verify_errorMsg = "", email_errorMsg = ""):
        self.render("signup.html", username = username,
                                email = email,
                                username_errorMsg =username_errorMsg,
                                password_errorMsg = password_errorMsg,
                                verify_errorMsg = verify_errorMsg,
                                email_errorMsg = email_errorMsg)
        
    def make_salt(self):
        return ''.join(random.choice(string.letters) for x in range(5))

class LoginHandler(AccountHandler):
    def get(self):
        self.render("login.html")

    def post(self):
    	username = self.request.get("username")
    	password = self.request.get("password")

    	# Verify username and password on database
    	db_users = Account.all()
    	db_users.filter("username =", username)
    	user_account = db_users.get()

    	if user_account == None:
    		self.render("login.html", login_errorMsg = "Invalid login")
    		return

    	user_account_hash = [user_account.password, user_account.salt]

    	if not self.valid_pw(username, password, user_account_hash):
    		self.render("login.html", login_errorMsg = "Invalid login")
    	else:
    		self.set_user_cookie(username)
    		self.redirect("/")

    def valid_pw(self, name, pw, h):
        salt = h[1]

        return h == self.make_pw_hash(name, pw, salt)


class LogoutHandler(AccountHandler):
    def get(self):
		self.clear_user_cookie()
		self.redirect("/login")
