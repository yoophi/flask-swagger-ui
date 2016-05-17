# -*- coding: utf8 -*-
import os
from urlparse import urlparse

import yaml
from flask import Blueprint, render_template, jsonify, current_app, url_for
from flask.ext.swagger import swagger

__version__ = '0.1'


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class SwaggerUI(Singleton):
    app = None
    params = {'OAUTH_CLIENT_ID': 'foo', 'OAUTH_CLIENT_SECRET': 'secret'}
    spec = {
        'info': {},
        'schemes': [],
        'produces': ['application/json'],
        'tags': [],
        'definitions': [],
        'securityDefinitions': [],
        'externalDocs': {}
    }

    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, info=None, spec=None, spec_yaml=None, url_prefix='/swagger', params={}):
        if spec:
            self.spec = dict(spec)

        if spec_yaml:
            self.spec = yaml.load(spec_yaml)

        if info:
            self.spec['info'].update(info)

        if params:
            self.params.update(params)

        app.register_blueprint(create_blueprint(__name__), url_prefix=url_prefix)


def spec():
    swag = swagger(current_app)
    swag.update(SwaggerUI().spec)
    swag.update({'host': get_netloc()})

    return jsonify(swag)


def oauth2callback():
    return render_template('o2c.html')


def swagger_ui_view():
    return render_template('swagger_ui.html',
                           swagger_spec_url=url_for('swagger_ui.spec', _external=True),
                           **SwaggerUI().params)


def get_netloc():
    parsed_url = urlparse(url_for('swagger_ui.spec', _external=True))
    return parsed_url.netloc


def create_blueprint(import_name):
    bp = Blueprint('swagger_ui', import_name, template_folder='templates',
                   static_folder='static', static_url_path='/static/swagger')
    bp.route('/spec', endpoint='spec')(spec)
    bp.route('/o2c.html', endpoint='o2c')(oauth2callback)
    bp.route('/', endpoint='swagger_ui')(swagger_ui_view)

    return bp
