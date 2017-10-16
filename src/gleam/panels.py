from jinja2 import Environment, PackageLoader
import os
import io
import hashlib
import base64
import random

import wtforms
from wtforms import Form
from wtforms.fields import Field
from wtforms.fields.core import UnboundField


class Panel(object):

    column_class = "col-md-4"

    def __init__(self):
        self.values = {}
        self.values["column_class"] = self.column_class

    def id(self):
        return self.name.replace(" ", "-").lower()

    def render(self):
        """Render the panel"""
        env = Environment(loader=PackageLoader('gleam', 'templates'))
        template = env.get_template(self.template_name)
        rendered = template.render(**self.values)
        return rendered


class InputPanel(Panel):
    """"An panel to display form inputs for the chart"""

    template_name = "input.html"

    def __init__(self):
        super(InputPanel, self).__init__()
        form_class = self.form_class()
        self.values["form"] = form_class(csrf_enabled=False)

    def form_class(self):
        """ Create an input form class with the fields in the panel class."""
        class InputForm(Form):
            extra = wtforms.fields.HiddenField()

        # get the fiel
        for name in self.__class__.__dict__:     
            if isinstance(getattr(self,name),UnboundField):
                setattr(InputForm,name,getattr(self,name))

        return InputForm


class TabPanel(Panel):

    template_name = "tabs.html"

    def __init__(self, tabs):
        self.tabs = tabs
        super(TabPanel, self).__init__()
        self.values["tabs"] = tabs

    def refresh(self, data):
        for tab in self.tabs:
            if tab.id() == data.extra:
                return tab.refresh(data)
        return {}


class PlotPanel(Panel):
    """A panel that contains a plot"""

    template_name = "plot.html"
    width = 700
    height = 500
    plotter = "matplotlib"
    extension = "png"
    name = "plot"

    def __init__(self):
        super(PlotPanel, self).__init__()
        self.values["height"] = self.height
        self.values["width"] = self.width
        self.values["name"] = self.name
        #self.plot_dir = os.path.join("static", "figures", self.name)
        #if not os.path.exists(self.plot_dir):
        #    os.makedirs(self.plot_dir)

    def __call__(self, func):
        """Using as a decorator"""
        self.func = func
        self.args = inspect.getargspec(func).args
        return self

    def refresh(self, data):
        """Generate a new image, then tell the page to change the src"""
        #cchane

        if self.plotter == "custom":
            kwargs["__outfile"] = outfile

        if self.plotter == "matplotlib":
            from matplotlib import pyplot as plt
            plt.clf()

        ret = self.plot(data)
        if ret is None:
            # don't change the plot at all
            return {self.name: {}}

        # after
        tempFile = io.BytesIO()
            
        if self.plotter == "matplotlib":
                
            plt.savefig(tempFile,format="png")
            
               
        elif self.plotter == "ggplot":
            from ggplot.utils import ggsave

            #ggsave(tempFile, ret)
            ret.save(tempFile) 
            tempFile.seek(0)
            base64encodedimage = base64.b64encode(tempFile.getvalue()).decode('utf8')

        # turn into a URL, add a dummy param to avoid browser caching
        tempFile.seek(0)
        base64encodedimage = base64.b64encode(tempFile.getvalue()).decode('utf8')
        tempFile.close()

        url = 'data:image/png;base64,'+ base64encodedimage

        return {self.name: {"src": url}}

    def __repr__(self):
        return self.render()
