#!/usr/bin/env python

from ..core import Service
from .models import Dossier


class DossiersService(Service):
    __model__ = Dossier
