#!/usr/bin/env python
"""
    app.core

    core module, wraps all the model stuff we might want
    to do into a nice class
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Service(object):
    __model__ = None

    def _isinstance(self, model):
        return isinstance(model, self.__model__)

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        if self._isinstance(model):
            db.session.add(model)
            db.session.commit()
            return model

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        if self._isinstance(model):
            for k, v in self._preprocess_params(kwargs).items():
                setattr(model, k, v)
            self.save(model)
            return model

    def delete(self, model):
        if self._isinstance(model):
            db.session.delete(model)
            db.session.commit()
