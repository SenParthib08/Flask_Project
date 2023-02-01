from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, template_folder='./templates')
# Setting a secret key for preventing attackers from changing the cookies..
app.config['SECRET_KEY'] = '4a55fdd370dc330fc456e31e7629c824'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# In SQLAlchemy the database can used as classes and objects in an intuitive way..
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_blog import routes