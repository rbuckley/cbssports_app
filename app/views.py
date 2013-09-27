#!/usr/bin/env python
from flask import request, render_template
from app import app, api
from app.forms import PlayerSelector, DossierTextField



@app.route('/', methods=['GET', 'POST'])
def index():
    if api.access_token is None:
        api.set_access_token(request.args.get('access_token'))

    players = api.players.list()

    selector = PlayerSelector(request.form)
    if selector.is_submitted():
        for p in selector.players.data:
            print api.players.search(player_id=p)

    selector.players.choices = [(p['id'], p['fullname']) for p in players['players']]

    return render_template('selector.html', form=selector)


@app.route('/dossier/<id>', methods=['GET', 'POST'])
def dossier(id=None):

    print 'opening dossier on ' + id

    form = DossierTextField(request.form)
    if form.validate_on_submit():
        print form.new_entry.data
        # do something with the data here
        # before we clear it
        form.new_entry.data = ''
        form.title.data = ''

    owners = api.league.owners()

    for x in owners['owners']:
        if x['id'] == id:
            owner = x

    return render_template('owner_profile.html', form=form, owner=owner)


@app.route('/dossier/', methods=['GET', 'POST'])
def home():
    owners = api.league.owners()

    return render_template('owners.html', owners=owners['owners'])
