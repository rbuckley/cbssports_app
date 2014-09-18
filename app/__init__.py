#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from cbssports import API

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = API()

from . import views, models
