#!/usr/bin/env python


from flask.ext.script import Command

from ..services import users


class DeleteAllUsersCommand(Command):

    def run(self):
        for u in users.all():
            users.delete(u)
