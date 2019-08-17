## ![](https://s3.amazonaws.com/python-ga/images/GA_Cog_Medium_White_RGB.png) 

<h1>Intro to Flask</h1>


**You will need the following** [frontend react app](https://git.generalassemb.ly/WebDev-Connected-Classroom/flask-api-user-profile/blob/master/README.md) - please clone


## Learning Objectives:
*After this lesson, you will be able to:*

- Write a basic Flask application.

---

## Discussion: Commonalities


What do you think these websites have in common?

- [Pinterest](http://www.pinterest.com)
- [Instagram](http://www.instagram.com)
- [LinkedIn](http://linkedin.com/)

They're each:

- High on user interactivity.
- Handling a large server load.

What else?

## They All Use **Flask**

![](https://qph.fs.quoracdn.net/main-qimg-cd83cf9ee7ad51b8af4d0c4d5220f534.webp)

Some quick notes about Flask:

- It's a Python micro web framework.
- It can create and write the entire back-end in Python!
- It can do small tasks (e.g., create a microblog or stand up a simple API).
- It can do complex tasks (e.g., Pinterest's API or create a Twitter clone).


<aside class="notes">

## Virtualenv

Let's also build a virtual environment. Virtual environments allow us to have multiple versions of Python on the same system so we can have different versions of both Python and the packages we are using on our computers.

- **clone this repo and cd into** `flask-api-user-profile`

```bash
$ pip3 install virtualenv
$ virtualenv .env -p python3
$ source .env/bin/activate
```


# flask-api-user-profile

1.  create a login/registration 
2.  create a user profile
3.  We are going to create a basic api that performs all crud routes updating a resource named dogs.
 



#### Setup virtualenv

- inside flask-api-user-profile folder
```bash
virtualenv .env -p python3
source .env/bin/activate
```

#### Dependencies

```bash
pip3 install flask-bcrypt peewee flask psycopg2 flask_login flask_cors
pip3 freeze > requirements.txt
```

We'll run the Flask app like any other app.

- We need to install Flask!
 Let's also install some dependencies and save them. Django doesn't utilize a `package.json`. Instead, we just use a text file that lists all of our dependencies. Pip freeze saves the dependencies in our `virtualenv` to that file. 
 
 
 If you are downloading and running a Python project, you can usually install its dependencies with `pip3 install -r requirements.txt`.


### Setup basic server 

```python
from flask import Flask

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
```

Run the app like normal:

`python app.py`

Go to:

`http://localhost:5000/`

You made a web app!

### Setting up User Model

##### Peewee the ORM

[Peewee](https://github.com/coleifer/peewee) - *Peewee is a simple and small ORM. It has few (but expressive) concepts, making it easy to learn and intuitive to use.* from the docs

This is the ORM (Object-relational mapping) we will use to hook up to our sql databases and communicate with them. 


```python
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('dogs.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    image = CharField()

    class Meta:
        database = DATABASE

class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Dog], safe=True)
    print("TABLES Created")
    DATABASE.close()

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Dog], safe=True)
    print("TABLES Created")
    DATABASE.close()
```

- We are using *sqlite* as our database here, this is really great for development purposes to get up and running real quick, later on we will connect to our production database postgres.

-  We are using the *UserMixin* here from [flask-login](https://flask-login.readthedocs.io/en/latest/), to give our User class some default features.  Mixins are small classes that add some specific feature. Since they're not the final class that we want to extend, they go at the beginning of our inheritance chain.


- *class Meta* - When Python creates a class object, special construction instructions can be provided. This is done through the Meta class. Since the database isn't part of the class itself, this class constructor information is provided through the special Meta class.

- The initialize method will set up our datatables, while we open and close the connection

- Now lets go to our app


```python
from flask import Flask

import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
```

- the `g` stands for global and we are setting up a global access to our database throughout the app. 

- when developing a web application, it’s common to open a connection when a request starts, and close it when the response is returned. You should always manage your connections explicitly. For instance, if you are using a connection pool, connections will only be recycled correctly if you call connect() and close().

We will tell flask that during the request/response cycle we need to create a connection to the database. Flask provides some useful decorators to make this easy

```python
@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response
 ```
 
 ##### Time to test it
 
- start the app - `python app.py`
 
- *What should you see?*

- in the console you should see `TABLES Created`

- this is coming from the initialize method which is in your models folder that you are invoking when you start the app

- *the method definition*
```python
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    print("TABLES Created")
    DATABASE.close()

```

- *invoking the method*

```python
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
```

### User Registration with a Profile Pic

###### React

- check out the code in the *React App*, notice the architecture and observer the `app.js` and `register.js`

- *Key things to Note*

1.  handling the upload of a file

```js
  handleChange = (e) => {
    if(e.target.name !== 'image'){
      this.setState({[e.target.name]: e.target.value});
    } else {
      // file upload
      console.log(e.target.files[0])
      this.setState({image: e.target.files[0]});
    }
  }
```

- jsx

```html
<Form.Input fluid icon='image' iconPosition='left' type="file" name='image' onChange={this.handleChange}/>
```
- You'll notice here that the files are attached to the target in an array on a property called `.files`.  and we are saving it in state.  In the jsx (or html) the `type='file'` the input type will always be `file`


##### API call

- register component

```js
handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append('file', this.state.image);
    data.append('username', this.state.username);
    data.append('password', this.state.password);
    data.append('email', this.state.email);

    console.log(data.entries(), ' this is data')
    for (let pair of data.entries()){
      console.log(pair[0]  ,', ', pair[1])
    }

    const registerCall = this.props.register(data);

    registerCall.then((data) => {
      console.log(data)
        if(data.status.message === "Success"){
          this.props.history.push('/profile')
        }
    })
  }
```

- You'll notice here that will have to create `FormData` in order to send over the file

- also remember async functions return promise's, so we can always call `.then` on them as we are in the following, 
- in order to switch the location of the routes

```js
registerCall.then((data) => {
      console.log(data)
        if(data.status.message === "Success"){
          this.props.history.push('/profile')
        }
    })

```

- The actual fetch call 

app.js

```js
const registerResponse = await fetch('http://localhost:8000/user/register', {
        method: 'POST',
        credentials: 'include',// on every request we have to send the cookie
        body: data,
        headers: {
          'enctype': 'multipart/form-data'
        }
      })
```

- In order for our flask app to be able to process the request with the file we have to make sure our headers have
the headers `'enctype': 'multipart/form-data'`.


### User Profile Resource (controller)

What we will do now is set up the register route, and create a user!  In Flask instead of controllers we will use resources!


*Whats a resource?* - The main building block provided by Flask-RESTful are resources, which gives us access our HTTP methods just by defining methods on your resource. A basic crud source looks like above.  

*BluePrints* - The basic concept of blueprints is that they record operations to execute when registered on an application. Flask associates view functions with blueprints when dispatching requests and generating URLs from one endpoint to another.

### resources 

```bash
mkdir resources
touch resources/init.py
touch resources/user.py
```

```python
import models

import os
import sys
import secrets

from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    ## This is how you get the image you sent over
    pay_file = request.files

    ## This has all the data like username, email, password
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()


    payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email']) # model query finding by email
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        file_picture_path = save_picture(dict_file['file']) # using the helper function to save the pic as a static file (i.e.
                                                            # helper function below 'save_picture'
        payload['image'] = file_picture_path # save the path to the file in the database
        user = models.User.create(**payload) # put the user in the database
                                             # **payload, is spreading like js (...) the properties of the payload object out
                                            


        #login_user
        login_user(user) # starts session

        current_user.image = file_picture_path # and the picture path so we have it whenever for the current_user
        ## convert class Model to class dict
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password'] # delete the password before we return it, because we don't need the client to be aware of it

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})
```

*Whats a resource?* - The main building block provided by Flask-RESTful are resources, which gives us access our HTTP methods just by defining methods on your resource. A basic crud source looks like above.  

*jsonify* - turning our python dictionaries into json.  

-  *BluePrints* - The basic concept of blueprints is that they record operations to execute when registered on an application. Flask associates view functions with blueprints when dispatching requests and generating URLs from one endpoint to another.

- `user = Blueprint('users', 'user', url_prefix='/user')` says treat this as a blueprint in the application (module) that we can attach to our flask app the will define a set of view functions.  


- `login_user` - comes from [flask login](https://flask-login.readthedocs.io/en/latest/) - this will intiate the session for us!

### Helper function save_picture

```python
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generate random integer for the name so no conflicts
    # won't use f_name
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_fn)

    output_size = (125, 175) # set the size of the picture
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.rotate(30)
    i.save(file_path_for_avatar)

    return picture_fn # return the picture name, so we can save it to the database
```

- [os](https://docs.python.org/3/library/os.html) - is a python module that gives you access to the file system

- [Pillow](https://pillow.readthedocs.io/en/stable/) - Pillow is a great module for saving/reading and manipulating images, the most important class that we'll `import` is the `Image` class.  This will allow us to process the picture (open) and save the picture.  

## Set up static folder to save profile pics

*at root (Same level as app.py)*
```
mkdir static
mkdir static/profile_pics
```

**Now we need to Register the Blueprint in the app.py and setup the login_manager**

```python
from flask import Flask, g
from flask_login import LoginManager
from flask_cors import CORS
import models

from api.api import api
from api.user import user

DEBUG = True
PORT = 8000

login_manager = LoginManager() # sets up the ability to set up the session


app = Flask(__name__, static_url_path="", static_folder="static")

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" ## Need this to encode the session
login_manager.init_app(app) # set up the sessions on the app

@login_manager.user_loader # decorator function, that will load the user object whenever we access the session
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)

```

- `config.secretkey` is for the hash for our session cookie we can make up whatever random characters we'd like. By default, Flask-Login uses sessions for authentication. This means you must set the secret key on your application,

-  We can use the `LoginManager()` to handle all the login things like is_authenticated, or get id. The login manager contains the code that lets your application and Flask-Login work together, such as how to load a user from an ID, and where to send users when they need to log in.  

-  `@login_manager.user_loader` - We need to provide user_loader callback. This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object.


- We also set up the login manager and setup cors to allow our react app to connect to our API's.  Notice we passed `supports_credentials=True` as well in order to give us the ability to send cookies back and forth.  



### Loading the pic in React!

*Profile Component*

```js
<Card
    image={'http://localhost:8000/profile_pics/' + this.props.userInfo.image}
    header={this.props.username}
    meta={this.props.email}
    description='most of the time I cant even be sure if she was ever with me'
    style={{'marginLeft': '5vw'}}
    />
 }
```

- notice here on the image property, we just put the route where it lives on the server since it is being rendered statically!

### Login

*api/user.py*


```python
@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '< --- this is playload')
    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
```

*Key things to note*

- ` payload = request.get_json()` - notice we are using `.get_json()` to retrieve the json from the route

- `user = models.User.get(models.User.email== payload['email'])` - our query to search by email

- `user_dict = model_to_dict(user)` - Use `model_to_dict` in order to read the model.  (The model is its own class)

- `check_password_hash(user_dict['password'], payload['password'])` - returns `True` or `False` depending on whether our hash's match

- `login_user(user)` - start the session and log in


# DOCS

- [flask](https://flask.palletsprojects.com/en/1.0.x/)
- [flask_login](https://flask-login.readthedocs.io/en/latest/#flask_login.current_user)
- [Pillow](https://pillow.readthedocs.io/en/stable/) (image processing)
- [PeeWee](http://docs.peewee-orm.com/en/latest/) (orm)
