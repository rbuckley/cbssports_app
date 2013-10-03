#!/usr/bin/env python

from ..core import db


class User(db.Model):
    """
        User model for our Dossier

        name:
            The name as retrieved from the owner api

        api_id:
            ID of the user who has installed the app, this
            will be the same across all leagues for this user

        dossiers:
            Child table that has one dossier for each league
            that this user is a part of.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    api_id = db.Column(db.String(36), unique=True)
    dossiers = db.relationship('Dossier', backref='user', lazy='dynamic')

    def __init__(self, api_id, name):
        self.api_id = api_id
        self.name = name
