#!/usr/bin/env python

from ..core import Service
from .models import User


class UsersServce(Service):
    __model__ = User
