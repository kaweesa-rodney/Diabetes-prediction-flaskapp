from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user
from app.models import Patient, User

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	if current_user.is_authenticated:
		return redirect(url_for('main.view'))
	#page = request.args.get('page', 1, type=int)
	#patient = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('index.html', title='Home')


@main.route("/about")
def about():
	return render_template("about.html", title='About')


@main.route("/view")
def view():
	page = request.args.get('page', 1, type=int)
	patients = Patient.query.order_by(Patient.date_posted.desc()).paginate(page=page)
	return render_template('view.html', patients=patients, title='Patients')