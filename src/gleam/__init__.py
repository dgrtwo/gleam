"""
Gleam: interactive visualizations in Python
"""

import os
import json
import urlparse
from collections import namedtuple

from flask import Flask, request, send_from_directory
from jinja2 import Environment, PackageLoader


GLEAM_STATIC_DIR = os.path.join(os.path.split(__file__)[0], "static")


class InputData(object):
    pass


class Page(object):
    @classmethod
    def add_flask(cls, app, path="/"):
        """Add this page to a Flask application at the given path"""

        env = Environment(loader=PackageLoader('gleam', 'templates'))

        panels_rendered = cls.input.render() + cls.output.render()

        # built-in static views
        @app.route('/gleam/<path:filename>')
        def custom_static(filename):
            return send_from_directory(GLEAM_STATIC_DIR, filename)

        # create main_view
        @app.route(path, methods=["GET"])
        def main_view():
            template = env.get_template('page.html')
            return template.render({'panels': panels_rendered})

        # create post view
        @app.route(path, methods=["POST"])
        def server_view():
            res = {}
            form_class = cls.input.form_class()
            form = form_class(request.form, csrf_enabled=False)
            if form.validate():
                # turn dictionary into an object
                d = InputData()
                d.__dict__.update(form.data)
                res = cls.output.refresh(d)
                return json.dumps({"changes": res})
            else:
                raise Exception("Form didn't validate")

    @classmethod
    def run(cls, debug=False, *args, **kwargs):
        """Create a Flask application with this single page"""
        app = Flask(cls.__name__)
        cls.add_flask(app)
        app.debug = debug
        app.run(*args, **kwargs)
