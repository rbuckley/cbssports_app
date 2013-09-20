#!/usr/bin/env python
import requests
import json

from flask import request

from app import app

@app.route('/')
def index():
    access_token = request.args.get('access_token')
    sport = request.args.get('SPORT')
    user_id = request.args.get('user_id')
    league_id = request.args.get('league_id')


    print access_token
    print sport
    print user_id
    print league_id
    r = requests.get('http://api.cbssports.com/fantasy/league/teams?version=2.0&request_format=JSON')
    r.json()
    return "Welcome to my cbssports app"
