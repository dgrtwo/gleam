import os
import unittest

from ggplot import *
from flask import Flask

from gleam import Page, widgets, outputs

class SimpleApp(Page):
    Title = "Meat Scatter Plot"

    xvar = widgets.Select(label="X axis", choices=["date"])
    yvar = widgets.Select(label="Y axis", choices=["beef", "pork"])
    smoother = widgets.Checkbox(label="Add Smoothing Curve?")
    title = widgets.Text(label="Title of plot:")

    @outputs.Plot(width=600, height=400, type="ggplot")
    def scatter_plot(xvar, yvar, smoother, title):
        p = ggplot(meat, aes(x=xvar, y=yvar))
        if smoother:
            p = p + stat_smooth()

        return p + geom_point() + ggtitle(title)


class TestSimpleApp(unittest.TestCase):
    """Test the server and client of SimpleApp"""
    def setUp(self):
        app = Flask("testapp")
        app.config['TESTING'] = True
        SimpleApp.add_flask(app, path="/gleam")
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_server(self):
        url = '/gleam/server?xvar=date&yvar=beef&smoother=false&title=Yay'
        res = self.app.get(url)
        print res.data


if __name__ == '__main__':
    unittest.main()
