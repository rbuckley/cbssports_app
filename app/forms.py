#!/usr/bin/env python

from flask_wtf import Form

from wtforms import SelectMultipleField, TextField, TextAreaField
from wtforms.validators import Required


class PlayerSelector(Form):
    players = SelectMultipleField('Players')


class DossierTextField(Form):
    title = TextField('Title', validators=[Required()])
    new_entry = TextAreaField('Entry', validators=[Required()], default='Write the dirt here...')
