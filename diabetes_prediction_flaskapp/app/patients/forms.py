from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired


class PatientForm(FlaskForm):
	pregnancies = IntegerField('Pregnancies', validators=[DataRequired()])
	glucose = IntegerField('Glucose', validators=[DataRequired()])
	bmi = IntegerField('BMI', validators=[DataRequired()])
	mychoices = [(0,0),(1,1),(2,2),(3,3)]
	pedigree_function = SelectField('Diabetes Pedigree Function', choices = mychoices, coerce=int )
	age = IntegerField('Age', validators=[DataRequired()])
	submit = SubmitField('Submit')