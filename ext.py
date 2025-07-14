from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

site = Flask(__name__)
site.config['SECRET_KEY'] = "utdgfxh1234567890@!?"
site.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(site)
login_manager = LoginManager(site)
login_manager.login_view = "home"