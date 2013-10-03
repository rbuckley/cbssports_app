#!/usr/bin/env python

from flask.ext.script import Manager

from app.api import create_app
from app.manage import DeleteAllUsersCommand, ListDossiers, DeleteDossier

manager = Manager(create_app())
manager.add_command('del_all_users', DeleteAllUsersCommand())
manager.add_command('list_dossiers', ListDossiers())
manager.add_command('del_dossier', DeleteDossier())

if __name__ == "__main__":
    manager.run()
