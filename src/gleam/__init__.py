"""
Gleam: interactive visualizations in Python
"""

import json

from flask import Flask, request
from jinja2 import Environment, PackageLoader

from widgets import Widget
from outputs import Output

class Page(object):
    @classmethod
    def add_flask(cls, app, path="/"):
        """Add this page to a Flask application at the given path"""
        # setup
        attrs = dict((n, getattr(cls, n)) for n in dir(cls))

        widgets = dict((k, v) for (k, v) in attrs.iteritems()
                            if isinstance(v, Widget))
        outputs = dict((k, v) for (k, v) in attrs.iteritems()
                            if isinstance(v, Output))

        env = Environment(loader=PackageLoader('gleam', 'templates'))

        for name, obj in widgets.items():
            obj.setup(name, env)
        for name, obj in outputs.items():
            obj.setup(name)

        # create main_view
        @app.route(path, methods=["GET"])
        def main_view():
            template = env.get_template('page.html')
            return template.render({'widgets': widgets.values(), 'outputs': outputs.values()})

        # create server_view
        @app.route(path + "/server", methods=["GET"])
        def server_view():
            res = {}

            # check we have all the values necessary for output method
            for name, o in outputs.iteritems():
                for a in o.args:
                    if a not in request.args:
                        raise ValueError(
                                "Value %s required for output %s not found" %
                                (a, name))

                args = dict((a, widgets[a].parse(request.args[a]))
                                for a in o.args)
                res[name] = o.refresh(**args)

            return json.dumps({"changes": res})


    @classmethod
    def run(cls, *args, **kwargs):
        """Create a Flask application with this single page"""
        app = Flask(cls.__name__)
        cls.add_flask(app)
        app.run(*args, **kwargs)
