# Flask modules:
# import everything from peewee
from peewee import * 
# flask_login helps set up users & sessions (like express sessions)
from flask_login import UserMixin

# pythod modules:
import datetime

# UserMixin is a "mini class" that we can inherit from that
# gives us special properties to help create sessions
# (pass this as a parameter to your User class)

# like mongoose.connect('mongodbString')
# connects to database
DATABASE = SqliteDatabase('dogs.sqlite')
# sqlite is just a file on our computer (lite SQL db)
# good for experimentation, getting things up and running
# (development).  Once models are set up,
# then you would add postgresql or mysql (production dbs)

# Set up the User model
# "Model" must be last class in parameter list
# Specialized classes (like UserMixin) go in front
# i.e., python allows instantiation with MULTPILE CLASSES! Unusual!
class User(UserMixin, Model):
	username = CharField()  # use unique=TRUE option in production
	email = CharField() # use unique=TRUE option in production
	password = CharField()
	image = CharField()

	# when the class object creates an object
	# can give it instructions with the Meta model
	class Meta:
		database = DATABASE

# when we initialize it, this will be of class model
class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

# this gets run from app.py when the app starts up
# (see models.initialize() invoking the function in app.py)
def initialize():
	# open connection to databse
	DATABASE.connect() 
	# create two tables: User and Dog 
	# (with columns as defined above)
	# safe=True prevents overwriting existing tables
	DATABASE.create_tables([User, Dog], safe=True)
	print("TABLES CREATED")
	# disconnect from db after writing (to save on resources)
	DATABASE.close()




