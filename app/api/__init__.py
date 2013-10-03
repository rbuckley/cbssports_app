#!/usr/bin/env python

from .. import factory


def create_app():

    app = factory.create_app(__name__)

    return app
