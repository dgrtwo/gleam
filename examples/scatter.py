from wtforms import fields
from ggplot import *

from gleam import Page, panels


class ScatterInput(panels.InputPanel):
    title = fields.StringField(label="Title of plot:")
    yvar = fields.SelectField(label="Y axis",
                              choices=[("beef", "Beef"),
                                       ("pork", "Pork")])
    smoother = fields.BooleanField(label="Smoothing Curve")


class ScatterPlot(panels.PlotPanel):
    name = "Scatter"

    def plot(self, inputs):
        p = ggplot(meat, aes(x='date', y=inputs.yvar))
        if inputs.smoother:
            p = p + stat_smooth(color="blue")
        p = p + geom_point() + ggtitle(inputs.title)
        return p


class ScatterPage(Page):
    input = ScatterInput()
    output = ScatterPlot()


ScatterPage.run()
