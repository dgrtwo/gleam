"""
Gleam: interactive visualizations in Python
"""

import json

from flask import Flask
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
        def main_view():
            pass                

        app.route(path, methods=["GET"])(cls.main_view)

        # create server_view
        def server_view():
            # call each output to refresh the page
            res = {}
            for name, o in outputs.iteritems():
                # check we have all the values necessary for output method
                for a in o.args:
                    if a not in request.args:
                        raise ValueError(
                                "Value %s required for output %s not found" %
                                (a, name))

                # to-do: set up outfile for plot objects
                res[name] = o.refresh(**dict((a, request.args[a])
                                                for a in o.args))
                

            return json.dumps({"changes": res})

        app.route(path + "/server", methods=["GET"])(cls.server_view)

    @classmethod
    def run(cls):
        """Create a Flask application with this single page"""
        app = Flask(cls.__name__)
        cls.add_flask(cls)
        return app
