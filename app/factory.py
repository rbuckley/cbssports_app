#!/usr/bin/env python

from flask import Flask
from core import db


def init_extensions(app):
    db.init_app(app)


def create_app(package_name, package_path):
    app = Flask(package_name)

    app.config.from_object('app.config')

    init_extensions(app)

    return app
