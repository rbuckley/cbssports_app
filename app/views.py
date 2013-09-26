#!/usr/bin/env python
import requests
import json

from flask import request

from app import app, api

@app.route('/')
def index():
    if api.access_token is None:
        api.set_access_token(request.args.get('access_token'))

    league_details = api.league.details()

    print league_details

    return "Welcome to my cbssports app"
