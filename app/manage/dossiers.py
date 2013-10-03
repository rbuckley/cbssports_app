#!/usr/bin/env python

from flask.ext.script import Command, prompt
from ..services import dossiers


class DeleteDossier(Command):

    def run(self):
        id = prompt('Id')
        dossier = dossiers.get(id)
        if not dossier:
            print 'Invalid Dossier id'
            return
        dossiers.delete(dossier)
        print 'Dossier deleted'

class ListDossiers(Command):
    """ list all dossiers in the database by id """
    def run(self):
        for d in dossiers.all():
            print 'Dossier id=%d' % d.id
