# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask, jsonify, request, url_for
from flask_swagger_ui import SwaggerUI

app = Flask(__name__)
swagger_ui = SwaggerUI(app,
                       spec={'info': {'title': 'Sample API', 'description': 'This is a demo page for ' '[Flask-Swagger-UI](https://github.com/yoophi/flask-swagger-ui).'}},
                       params={})


@app.route('/sample')
def handle_sample():
    """
    Sample API
    This is a sample API for Flask-Swagger-UI.
    ---
    parameters:
      - name: name
        in: query
        description: 고객 이름
        type: string
    tags:
      - Sample
    responses:
      200:
        description: OK
        schema:
          type: object
          properties:
            name:
              type: string
            data:
              type: string
    """
    name = request.args.get('name', 'undefined')
    return jsonify({
        'name': name,
        'data': 'Hello, %s' % (name,)
    })


@app.route('/')
def index():
    return '<a href="%s">Go to SwaggerUI page.</a>' % url_for('swagger_ui.swagger_ui')


if __name__ == '__main__':
    app.run(debug=True)
