# this is like the controller in express

import models      # imports the models.py file
						 # which contains models.Dog, models.User
import os
import sys
import secrets
from PIL import Image

# Blueprint: record operations to execute (controllers)
# request: bopy of requests
# jsonify: send returns to requests as JSON
from flask import Blueprint, request, jsonify, url_for, send_file
# to hash passwords and check for password match
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
# change a model instance of a class to a dictionary
from playhouse.shortcuts import model_to_dict

# set up blueprint 
# blueprint name, import name, route prefix
# (this will have to be registered in app.py file)
user = Blueprint('users', 'user', url_prefix='/user')

# purpose of the function is to save the image as a static asset
# in folder static/profile_pics
# uses the modules pillow (PIL) and os (operating system)
def save_picture(form_picture):
	# 1. generate random integer for the name so no file name conflicts
	random_hex = secrets.token_hex(8) 
	# split file into tow parts: filename + extension
	# grab the file extension (.jpeg, .jpg, .png,...)
	# actually not grabbing f_name here (since will generate random name next)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	# create a random picture name with the correct extensions
	picture_fname = random_hex + f_ext
	# create the file path
	file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_fname)

	# pillow (PIL) module stuff
	output_size = (125, 175) # set the size of the picture
	# open the file sent from the client
	i = Image.open(form_picture)
	# set the size (takes a tuple as input)
	i.thumbnail(output_size)
	# I guess you can play around a bit with the pic before saving it
	# (i.e., more than just the file size above)
	i.rotate(30)
	# save the file to the path we set up (in the static folder)
	i.save(file_path_for_avatar)

	# return the picture file name so we can save that in the db
	return picture_fname 

@user.route('/register', methods=['POST'])
def register():
	# this is how we grab the image being sent over
	pay_file = request.files
	# this has the form info in the dict
	# we change the request object to a dictionary
	# so we can see inside it
	payload = request.form.to_dict()
	dict_file = pay_file.to_dict()

	print(payload)
	print(dict_file)

	payload['email'].lower()   # make emails all lower case!

	# See if email exists, if it does, let user know
	try:
		# query to try to find user by their email
		models.User.get(models.User.email == payload['email'])
		# if models.User.get exists, let user know that email is taken
		return jsonify(data={}, status={"code": 401, "message": "A user with that name or email already exists"})
	except models.DoesNotExist: # boolean on the model

		# otherwise, create and register user

		# hash password using bcrypt
		payload['password'] = generate_password_hash(payload['password'])

		# this function will save image as a static asset in static folder
		file_picture_path = save_picture(dict_file['file'])
		# (save_picture is a helper function we will create)

		# add image property to the payload dictionary and
		# save the file path there for db storage of file path (not image)
		payload['image'] = file_picture_path

		# this is an instance of the class User (an object)
		# (will convert to dictionary soon with model_to_dict module)
		user = models.User.create(**payload)

		print(type(user))  # type = class

		# ** is like spread operator in JS
		# so we don't have to type all of this:
		# user = models.User.create(username=payload['username'], password=payload['password'], ...and so on)

		# start the user session
		login_user(user)  # login_user is from flask_login module
		# login_user will set user id in session 
		# (and we can now refer to current_user)

		current_user.image = file_picture_path

		# we cannot send back a class (use model_to_dict module)
		# want response object to be "jsonifyable"
		# e.g., lists, dictionaries, booleans, strings, numbers,...
		user_dict = model_to_dict(user)
		print(user_dict)
		print(type(user_dict))  # now type = dict

		# remove password, client doesn't need to know
		del user_dict['password']

		return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

	return 'hi from register'


