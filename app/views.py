#!/usr/bin/env python

from flask import request, render_template
from app import app, api, db, models
from app.forms import PlayerSelector, DossierTextField


@app.route('/', methods=['GET', 'POST'])
def index():
    if api.access_token is None:
        api.set_access_token(request.args.get('access_token'))
    return render_template('base.html')

@app.route('/report', methods=['GET', 'POST'])
def advReport():

    players = api.players.list()

    selected_players = []
    selector = PlayerSelector(request.form)
    if selector.is_submitted():
        for p in selector.players.data:
            selected_players += api.players.search(player_id=p)['players']
            print api.general.stats(player_id=p, timeframe='2014', period='season')
            print api.league.fantasy__points(player_id=p, timeframe='2014', period='season')

    selector.players.choices = [(p['id'], p['fullname'])
                                for p in players['players']]

    return render_template('selector.html', form=selector,
                           selected_players=selected_players)


@app.route('/dossier/<id>', methods=['GET', 'POST'])
def individualDossier(id=None):
    owners = api.league.owners()['owners']
    for x in owners:
        if x['id'] == id:
            owner = x

    owner_page = models.Page.query.filter_by(owner_id=owner['id']).first()

    form = DossierTextField(request.form)
    if form.validate_on_submit():
        # do something with the data here
        # before we clear it

        new_page = models.Entry(owner_page.id,
                                form.title.data, form.new_entry.data)
        db.session.add(new_page)
        db.session.commit()
        form.new_entry.data = ''
        form.title.data = ''

    entries = []
    if owner_page is not None:
        entries = owner_page.entries.all()
    return render_template('owner_profile.html',
                           form=form, owner=owner, entries=entries)


@app.route('/dossier/', methods=['GET', 'POST'])
def dossiers():
    owners = [x for x in api.league.owners()['owners']
              if 'logged_in_owner' not in x]

    return render_template('owners.html', owners=owners)


@app.route('/teams/', methods=['GET', 'POST'])
def teams():
    return render_template('base.html')
