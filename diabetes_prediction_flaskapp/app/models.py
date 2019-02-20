from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	imagefile = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	patients = db.relationship('Patient', backref='author', lazy=True)


	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod	
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)



	def __repr__(self):
		return "User('%s', '%s', '%s')" % (self.username, self.email, self.imagefile)

class Patient(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pregnancies = db.Column(db.Integer, nullable=False)
	glucose = db.Column(db.Integer, nullable=False)
	bmi = db.Column(db.Integer, nullable=False)
	pedigree_function = db.Column(db.Integer, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	outcome = db.Column(db.Integer, nullable=False)


	def __repr__(self):
		return "Patient('%s','%s','%s','%s','%s','%s','%s')" % (self.pregnancies, self.glucose, self.bmi,
																 self.pedigree_function, self.age, self.date_posted,
																 self.user_id)