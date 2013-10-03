#!/usr/bin/env python

from flask import Blueprint, request

bp = Blueprint('dossiers', __name__, url_prefix='/dossier')


@bp.route('/')
def owners():

