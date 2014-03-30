from jinja2 import Environment, PackageLoader
import os
import hashlib

import wtforms
from wtforms import Form
from wtforms.fields import Field
from wtforms.fields.core import UnboundField

class Panel(object):

    column_class = "col-md-4"
    
    def __init__(self):
        self.values = {}
        self.values["panel"] = self
        self.values["column_class"] = self.__class__.column_class

    def id(self):
        return self.name.replace(" ", "-").lower()

    def render(self):
        """Render the panel"""
        env = Environment(loader=PackageLoader('gleam', 'templates'))
        template = env.get_template(self.template_name)
        rendered = template.render(**self.values)  
        return rendered


class Inputs(Panel):
    """"An panel to display form inputs for the chart"""
    
    template_name = "input.html"

    def __init__(self):
        super(Inputs, self).__init__()
        form_class = self.form_class()
        self.values["form"] = form_class(csrf_enabled=False)
        
    def form_class(self):
        """ Create an input form class with the fields in the panel class."""
        class InputForm(Form):
            extra = wtforms.fields.HiddenField()
            
        # get the fields
        for name, obj in self.__class__.__dict__.iteritems():
            if isinstance(obj, UnboundField):
                setattr(InputForm, name, obj)

        return InputForm


class Tabs(Panel):
    
    template_name = "tabs.html"
    
    def __init__(self):
        super(Tabs, self).__init__()
        self.values["tabs"] = self.tabs
        
    def refresh(self, data):
        for tab in self.tabs:
            if tab.name == data.extra:
                return tab.refresh(data)
        return {}
        

class Plot(Panel):
    """A panel that contains a plot"""
    
    template_name = "plot.html"
    width = 600
    height = 600
    plotter = "ggplot"
    extension = "png"
    name = "plot"

    def __init__(self):
        super(Plot, self).__init__()
        self.values["height"] = self.__class__.height
        self.values["width"] = self.__class__.width
        self.values["name"] = self.__class__.name
        self.plot_dir = os.path.join("static", "figures", self.__class__.name)
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)

    def __call__(self, func):
        """Using as a decorator"""
        self.func = func
        self.args = inspect.getargspec(func).args
        return self

    def refresh(self, data):
        """Generate a new image, then tell the page to change the src"""
        h = hashlib.md5(str(data.__dict__)).hexdigest()
        print h

        outfile = os.path.join(self.plot_dir, h + "." + self.extension)

        if not os.path.exists(outfile):

            if self.plotter == "custom":
                kwargs["__outfile"] = outfile

            if self.plotter == "matplotlib":
                from matplotlib import pyplot as plt
                plt.clf()
            
            ret = self.plot(data)

            # after
            if self.plotter == "matplotlib":
                plt.savefig(outfile)
            elif self.plotter == "ggplot":
                from ggplot.utils import ggsave
                ggsave(outfile, ret)

        return {self.__class__.name: {"src": outfile.replace("\/", "/")}}

    def __repr__(self):
        return self.render()
