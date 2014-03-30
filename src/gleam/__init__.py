"""
Gleam: interactive visualizations in Python
"""

import json
import urlparse

from flask import Flask, request
from jinja2 import Environment, PackageLoader

from outputs import Output
from flask_wtf import Form
from wtforms.fields import Field
from wtforms.fields.core import UnboundField

class Page(object):
    @classmethod
    def add_flask(cls, app, path="/"):
        """Add this page to a Flask application at the given path"""
        # setup
        server_path = '/'.join([u.strip('/') for u in [path, "server"]])
        attrs = dict((n, getattr(cls, n)) for n in dir(cls))
        fields = dict((k, v) for (k, v) in attrs.iteritems()
                            if isinstance(v, UnboundField))                            
        outs = dict((k, v) for (k, v) in attrs.iteritems()
                            if isinstance(v, Output))
                
                        
        env = Environment(loader=PackageLoader('gleam', 'templates'))

        class InputForm(Form):
            pass
                    
        for name, obj in fields.items():
            setattr(InputForm, name, obj)
                    
        for name, obj in outs.items():
            obj.setup(name, env)

        # create main_view
        @app.route(path, methods=["GET"])
        def main_view():
            form = InputForm(csrf_enabled=False)
            template = env.get_template('page.html')
            return template.render({'title': cls.pageTitle,
                                    'form': form, 
                                    'outputs': outs.values(),
                                    'server_path': server_path})

        # create server_view
        @app.route(server_path, methods=["POST"])
        def server_view():
            res = {}

            form = InputForm(csrf_enabled=False)
            if form.validate_on_submit():
                for name, o in outs.iteritems():
                    args = dict((a, form.data[a]) for a in o.args)
                    res[name] = o.refresh(**args)
                return json.dumps({"changes": res})
            else:
                import pdb; pdb.set_trace()
                abort()

            # check we have all the values necessary for output method
            """for name, o in outs.iteritems():
                #args = dict((a, request.args[a]) for a in o.args)
                args = dict((a, fields[a].parse(request.args))
                                for a in o.args)
                res[name] = o.refresh(**args)

            return json.dumps({"changes": res})"""


    @classmethod
    def run(cls, *args, **kwargs):
        """Create a Flask application with this single page"""
        app = Flask(cls.__name__)
        cls.add_flask(app)
        app.run(*args, **kwargs)
