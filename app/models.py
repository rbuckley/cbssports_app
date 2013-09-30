#!/usr/bin/env python

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    api_id = db.Column(db.String(36), unique=True)
    dossiers = db.relationship('Dossier', backref='user', lazy='dynamic')

    def __init__(self, api_id, name):
        self.api_id = api_id
        self.name = name


class Dossier(db.Model):
    __tablename__ = 'dossiers'
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.String)
    owner_pages = db.relationship('Page', backref='dossier', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Page(db.Model):
    """
        This is the main focus of the Dossier, this will contain
        all the information on ONE opponent in the league
        The Dossier will be made up of many of these

        entries:
            Blog post type blurbs about anything

        loves:
            List of player ids we think this owner loves

        hates:
            List of player ids we think this owner hates
    """
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    entries = db.relationship('Entry', backref='dossier', lazy='dynamic')
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'))
    loves = db.Column(db.Text)
    hates = db.Column(db.Text)


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
