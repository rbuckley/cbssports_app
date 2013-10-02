#!/usr/bin/env python
from flask import request, render_template
from app import app, api
from app.forms import PlayerSelector, DossierTextField

from app import db, models

@app.route('/', methods=['GET', 'POST'])
def index():
    api.set_access_token(request.args.get('access_token'))

    user_id = request.args.get('user_id')
    league_id = request.args.get('league_id')

    u = models.User.query.filter_by(api_id=user_id).first()
    #u = models.User.query.get(user_id)
    if u is None:
        # need to create a new user
        # get the JSON object from the API
        owners = api.league.owners()['owners']
        for x in owners:
            if 'logged_in_owner' in x:
                owner = x
        create_new_user(owner, user_id, league_id)
    elif u.dossiers.filter_by(league_id=league_id).first() is None:
        create_new_dossier(league_id, u.id)

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
        new_page = models.Entry(owner_page.id, form.title.data, form.new_entry.data)
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


def create_new_user(owner, user_id, league_id):

    new_user = models.User(user_id, owner['name'])
    db.session.add(new_user)
    db.session.commit()

    dossier = create_new_dossier(league_id, new_user.id)

    return new_user


def create_new_dossier(league_id, user_id):
    dossier = models.Dossier(league_id, user_id)
    db.session.add(dossier)
    db.session.commit()

    # get the list of owners not us
    owners = [x for x in api.league.owners()['owners']
              if 'logged_in_owner' not in x]

    # create the initial page for each rival owner
    for owner in owners:
        db.session.add(models.Page(
            dossier.id, owner['id'], owner['team']['id']))

    db.session.commit()

    return dossier
