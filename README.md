# Flask-Swagger-UI

Flask 어플리케이션의 API 문서화를 쉽게 구성해주는 extension 입니다.
`Flask-Swagger`를 내부적으로 호출하여 `spec` 문서를 생성하고, 그 문서를 `Swagger.ui` 뷰어를 이용해 볼 수 있는 페이지를 제공합니다.

서비스가 OAuth 2.0 방식의 인증 기능을 제공하는 경우, `Swagger.ui` 문서 내에서 토큰발행 및 `Bearer Token`을 이용한 API 호출 기능을 사용할 수 있습니다.


## 설치 


```
$ pip install https://github.com/yoophi/flask-swagger-ui.git
```

## 사용 방법 


`SwaggerUI` 클래스를 이용해 Flask APP 을 초기화합니다. 이후 
`Flask-Swagger` 방식으로 API method 에 docstring 을 달아놓으면 됩니다.

APP 을 실행한 후 <http://localhost:5000/swagger> 에서 문서를 사용할 수 있습니다.

```
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
```

위 예제는 `/example` 디렉토리에서 확인할 수 있습니다.


## OAuth2.0 인증 기능 사용 

예제를 준비중입니다.