from flask import Flask, g  
# g stands for global variables (variables provided by Flask)
from flask_cors import CORS
from flask_login import LoginManager


# all the classes and functions are methods on the models object
# (User and Dog classes, initialize() method)
import models # import the models.py file

# import the blueprint
from api.user import user

DEBUG = True
PORT = 8000

login_manager = LoginManager() # sets up the ability to set up the session

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__, static_url_path="", static_folder="static")
# like for express:
# const app = express()

#############################################################################
# Need to hide this elsewhere!
# password hash key
app.secret_key = 'RKAADGJASDFK RANDOM STRING'
#############################################################################

# sets up the session on the app
login_manager.init_app(app)

# decorator for current user or load anything from the session
@login_manager.user_loader # decorator function, that will load the user object whenever we access the session
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

# sets up the blueprint (controller) in the server file
app.register_blueprint(user)

# "decorator" (anything with an @ is a decorator)
# and its a function before a function

# connect to database before each query/request
@app.before_request # given to us by flask @
def before_request():
	"""Connect to the database before each request"""
	g.db = models.DATABASE
	g.db.connect()

# close connection to database after each query/request
@app.after_request # given to us by flask @
def after_request(response):
	"""Close connection to the database after each request"""
	g.db = models.DATABASE
	g.db.close()
	return response

# The default URL ends in / ("my-website.com/").
# this is a get route (default is GET)
@app.route('/')  
def index():  # can name this method whatever you like
    return 'hello world' # like "res.send" in express

# can also be something like this in other routes:
# @app.route('route/<param>')
# @app.route('alligators/<id>')
# @app.route('/', methods=['POST'])

# like for express:
# app.get('/', (req, res) => {
# 	...
# })

# Run the app when the program starts!
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT) # like app.listen in express



