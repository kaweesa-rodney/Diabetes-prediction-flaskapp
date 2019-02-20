from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Patient
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, 
								ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to Log In', 'success')
		return redirect(url_for('users.login'))
	return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.view'))
		else:
			flash('Login Unsuccessful! Please try again', 'danger')

	return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('users.login'))

@users.route("/account" ,methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.imagefile = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method =='GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	imagefile = url_for('static', filename='profile_pics/' + current_user.imagefile)
	return render_template("account.html", title="Account", imagefile=imagefile, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	patients = Patient.query.filter_by(author=user)\
		.order_by(Patient.date_posted.desc())\
		.paginate(page=page, per_page=5)
	return render_template('user_posts.html', patients=patients, user=user)


@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email has been sent with instructions to reset your password.", 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to Log In', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title="Reset Password", form=form)
