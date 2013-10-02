#!/usr/bin/env python

from flask import request, render_template
from app import app, api, db, models
from app.forms import PlayerSelector, DossierTextField

from app.session import Session

@app.route('/', methods=['GET', 'POST'])
def index():
    api.set_access_token(request.args.get('access_token'))

    user_id = request.args.get('user_id')
    league_id = request.args.get('league_id')

    # this will create the session we can use for the
    # remainder of the time the user is logged in
    # it provides methods for getting anything out
    # of the database
    dossier_sesh = Session(user_id, league_id)

    players = api.players.list()

    selector = PlayerSelector(request.form)
    if selector.is_submitted():
        for p in selector.players.data:
            print api.players.search(player_id=p)

    selector.players.choices = [(p['id'], p['fullname'])
                                for p in players['players']]

    return render_template('selector.html', form=selector)


@app.route('/dossier/<id>', methods=['GET', 'POST'])
def dossier(id=None):
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
def home():
    owners = [x for x in api.league.owners()['owners']
              if 'logged_in_owner' not in x]

    return render_template('owners.html', owners=owners)
