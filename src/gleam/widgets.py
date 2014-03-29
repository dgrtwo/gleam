"""
Widgets are inputs in HTML/CSS/JS
"""

import os
import ast


class Widget(object):
    """Overall widget class"""
    def __init__(self, values):
        self.values = values

    def setup(self, name, env):
        """Takes a jinga2 environment"""
        self.name = name
        self.values["name"] = name

        # template = env.get_template(os.path.join('widgets',self.Template))
        template = env.get_template(self.Template)
        self.rendered = template.render(**self.values)        
    
    def parse(self, args):
        return args[self.name]

    def __repr__(self):
        return self.rendered


class Slider(Widget):
    """Slider for continuous values"""

    def __init__(self, label, minimum, maximum, value, step=1):
        d = {"label": label, "minimum": minimum, "maximum": maximum,
             "value": value, step: "step"}
        Widget.__init__(self, d)

    def parse(self, args):
        return ast.literal_eval(args[self.name])


class Checkbox(Widget):
    """Checkbox for boolean input"""
    Template = "checkbox.html"

    def __init__(self, label, default=False):
        self.default = default
        Widget.__init__(self, {"label": label, "default": default})

    def parse(self, args):
        return self.name in args


class Select(Widget):
    """Select between choices"""
    Template = "select.html"

    def __init__(self, label, choices, default=None):
        """By default, use the first choice"""
        d = {"label": label, "choices": choices, "default": default}
        Widget.__init__(self, d)


class Text(Widget):
    """Text box"""
    Template = "text.html"

    def __init__(self, label, default="", maxchar=100):
        d = {"label": label, "default": default, "maxchar": maxchar}
        Widget.__init__(self, d)
