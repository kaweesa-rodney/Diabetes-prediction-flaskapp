import os
from os import urandom
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
#from app import mail

def save_picture(form_picture):
	random_hex = urandom(8).hex()
	f_name,f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics/',picture_fn)

	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	stuff = url_for('users.reset_token', token=token, _external=True)

	msg.body = '''To reset your password, visit the following link:
	{%s}
	 If your did not make this request then simply ignore this email and no changes will be made
	''' % stuff
	#mail.send(msg)
