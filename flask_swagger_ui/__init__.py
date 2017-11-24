# -*- coding: utf8 -*-
from urlparse import urlparse

import yaml
from flask import Blueprint, render_template, jsonify, current_app, url_for
from flask_swagger import swagger, _parse_docstring, _sanitize

__version__ = '0.1.5'


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class SwaggerUI(Singleton):
    app = None
    params = {'OAUTH_CLIENT_ID': 'swagger',
              'OAUTH_CLIENT_SECRET': 'secret',
              'LOGO_TITLE': 'swagger', }
    spec = {
        'info': {},
        'schemes': [],
        'produces': ['application/json'],
        'tags': [],
        'definitions': [],
        'securityDefinitions': [],
        'externalDocs': {},
    }

    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app,
                 info=None,
                 oauth_authorize=None,
                 oauth_access_token=None,
                 spec=None,
                 spec_yaml=None,
                 url_prefix='/swagger',
                 hide_in_production=True,
                 params={}):

        if not hide_in_production or app.config['DEBUG']:
            if spec:
                self.spec = dict(spec)

            if spec_yaml:
                self.spec = yaml.load(spec_yaml)

            if info:
                self.spec['info'].update(info)

            if params:
                self.params.update(params)

            app.register_blueprint(
                create_blueprint(__name__,
                                 oauth_authorize=oauth_authorize,
                                 oauth_access_token=oauth_access_token),
                url_prefix=url_prefix)

    def add_schema(self, schema_class):
        """
        schema class 의 내용을 추출하여 swagger spec 에 추가한다.
        :param schema_class:
        :return:
        """
        name, _, swag = _parse_docstring(schema_class, _sanitize)
        self.spec['definitions'][name] = swag


def spec():
    prefix = current_app.config.get('SWAGGER_UI_API_PREFIX', None)

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


def create_blueprint(import_name, oauth_authorize=None, oauth_access_token=None):
    bp = Blueprint('swagger_ui', import_name, template_folder='templates',
                   static_folder='static', static_url_path='/static/swagger')
    bp.route('/spec', endpoint='spec')(spec)
    bp.route('/o2c.html', endpoint='o2c')(oauth2callback)
    bp.route('/', endpoint='swagger_ui')(swagger_ui_view)

    if oauth_authorize and oauth_access_token:
        def setup_oauth_url():
            authorize_url = url_for(oauth_authorize, _external=True)
            access_token_url = url_for(oauth_access_token, _external=True)
            SwaggerUI().spec["securityDefinitions"]["oauth"]["authorizationUrl"] = authorize_url
            SwaggerUI().spec['info']['description'] = SwaggerUI().spec['info']['description'].replace(
                '{{OAUTH_AUTHORIZE_URL}}', access_token_url)

        bp.before_app_first_request(setup_oauth_url)

    return bp
