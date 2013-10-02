#!/usr/bin/env python

from app import db, models

models.Dossier.query.delete()
models.Entry.query.delete()
models.Page.query.delete()
models.User.query.delete()

db.session.commit()
