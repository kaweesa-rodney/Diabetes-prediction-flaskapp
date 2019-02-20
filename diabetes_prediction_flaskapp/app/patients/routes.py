from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, Markup)
from flask_login import current_user, login_required
from app import db
from app.models import Patient
from app.patients.forms import PatientForm
import pickle
import numpy as np


patients = Blueprint('patients', __name__)


@patients.route("/patient/new", methods=['GET','POST'])
@login_required
def new_patient():
	form = PatientForm()
	if form.validate_on_submit():

		preg = int(form.pregnancies.data)
		gluc = int(form.glucose.data)
		bm = int(form.bmi.data)
		pedigree = int(form.pedigree_function.data)
		ag = int(form.age.data)
		arr = np.array([[preg,gluc,bm,pedigree,ag]])
		#loading model
		loaded_model = pickle.load(open('../second_diabetes_classification_model.sav', 'rb'))
		result = loaded_model.predict(arr)
		
		if result[0] == 1:
			output = 1
			word = "Patient likely to be Diabetic"
		else:
			output = 0
			word = "Patient not Diabetic"

		patient = Patient(pregnancies=form.pregnancies.data, glucose=form.glucose.data, 
							bmi=form.bmi.data, pedigree_function=form.pedigree_function.data,
							age=form.age.data ,author=current_user, outcome=output)

		

		db.session.add(patient)
		db.session.commit()
		msg = Markup("Patient data has been added successfully, Prediction for added patient: <b><u>"+ word + "</u></b>")
		flash(msg, 'success')

		return redirect(url_for('main.view'))
	return render_template("create_patient.html", title="New Patient", form=form, legend = 'New Patient')


@patients.route("/patient/<int:patient_id>")
def patient(patient_id):
	patient = Patient.query.get_or_404(patient_id)
	return render_template('patient.html', title='Patient', patient=patient)


@patients.route("/patient/<int:patient_id>/update", methods=['GET','POST'])
@login_required
def update_patient(post_id):
	patient = Patient.query.get_or_404(patient_id)
	if patient.author != current_user:
		abort(403)
	form = PatientForm()
	if form.validate_on_submit():
		patient.pregnancies = form.pregnancies.data
		patient.glucose = form.glucose.data
		patient.bmi = form.bmi.data
		patient.pedigree_function = form.pedigree_function.data
		patient.age = form.age.data
		db.session.commit()
		flash('Patient data has been updated!', 'success')
		return redirect(url_for('patients.patient', patient_id=patient.id))
	elif request.method == 'GET':
		form.pregnancies.data = patient.pregnancies
		form.glucose.data = patient.glucose
		form.bmi.data = patient.bmi
		form.pedigree_function.data = patient.pedigree_function
		form.age.data = patient.age
	return render_template("create_patient.html", title="Update Patient", form = form, legend='Update Patient Data')


@patients.route("/patient/<int:patient_id>/delete", methods=['POST'])
@login_required
def delete_patient(patient_id):
	patient = Patient.query.get_or_404(patient_id)
	if patient.author != current_user:
		abort(403)
	db.session.delete(patient)
	db.session.commit()
	flash('Patient data been deleted','success')
	return redirect(url_for('main.home'))



