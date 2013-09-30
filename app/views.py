#!/usr/bin/env python
from flask import request, render_template
from app import app, api
from app.forms import PlayerSelector, DossierTextField

from app import db, models

@app.route('/', methods=['GET', 'POST'])
def index():
    if api.access_token is None:
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

    print 'opening dossier on ' + id

    form = DossierTextField(request.form)
    if form.validate_on_submit():
        print form.new_entry.data
        # do something with the data here
        # before we clear it
        form.new_entry.data = ''
        form.title.data = ''

    owners = api.league.owners()['owners']

    for x in owners:
        if x['id'] == id:
            owner = x

    return render_template('owner_profile.html', form=form, owner=owner)


@app.route('/dossier/', methods=['GET', 'POST'])
def home():
    owners = api.league.owners()

    return render_template('owners.html', owners=owners['owners'])


def create_new_user(owner, user_id, league_id):

    new_user = models.User(user_id, owner['name'])
    db.session.add(new_user)
    db.session.commit()

    # create the Dossier object for this league
    dossier = models.Dossier(league_id, new_user.id)

    db.session.add(dossier)
    db.session.commit()
    print 'created new dossier[%s] for league %s' % (dossier.id, dossier.league_id)
    # get the list of owners not us
    owners = [x for x in api.league.owners()['owners']
              if 'logged_in_owner' not in x]

    # create the initial page for each rival owner
    for owner in owners:
        print 'adding new page for %s[%s]' % (owner['name'], owner['id'])
        db.session.add(models.Page(
            dossier.id, owner['id'], owner['team']['id']))

    db.session.commit()
