#!/usr/bin/env python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

CSRF_ENABLE = True
SECRET_KEY = 'shhh_its_a_secret'
