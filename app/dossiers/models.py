#!/usr/bin/env python
from ..core import db


class Dossier(db.Model):
    __tablename__ = 'dossiers'
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner_pages = db.relationship('Page', cascade='all, delete', backref='dossier', lazy='dynamic')

    def __init__(self, league_id, user_id):
        self.league_id = league_id
        self.user_id = user_id


class Page(db.Model):
    """
        This is the main focus of the Dossier, this will contain
        all the information on ONE opponent in the league
        The Dossier will be made up of many of these

        entries:
            Blog post type blurbs about anything

        dossier_id:
            Reference back up to the dossier table

        owner_id:
            The CBS id for this owner as returned by the api

        team_id:
            The CBS is for this team as returned by the api

        loves:
            List of player ids we think this owner loves

        hates:
            List of player ids we think this owner hates
    """
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    entries = db.relationship('Entry', cascade='all, delete', backref='dossier', lazy='dynamic')
    owner_id = db.Column(db.String(36))
    team_id = db.Column(db.Integer)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'))
    loves = db.Column(db.Text)
    hates = db.Column(db.Text)

    def __init__(self, dossier_id, owner_id, team_id):
        self.dossier_id = dossier_id
        self.owner_id = owner_id
        self.team_id = team_id


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

    def __init__(self, page_id, title, body):
        self.page_id = page_id
        self.title = title
        self.body = body
