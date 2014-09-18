#!/usr/bin/env python

from flask import Blueprint

bp = Blueprint('dossiers', __name__, url_prefix='/dossier')


@bp.route('/')
def owners():
    return "hello world"
