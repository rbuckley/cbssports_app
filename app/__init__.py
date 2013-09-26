#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from cbssports import API

app = Flask(__name__)
db = SQLAlchemy(app)
api = API('JSON')

from app import views, models
