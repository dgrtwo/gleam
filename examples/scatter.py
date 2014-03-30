from flask import Flask
from gleam import Page, panels, outputs
from wtforms import fields

from ggplot import meat, aes, stat_smooth, geom_point, ggtitle, ggplot

class GleamInput(panels.Inputs):
    smoother = fields.BooleanField(label="Smoothing Curve")
    title = fields.StringField(label="Title of plot:")
    yvar = fields.SelectField(label="Y axis",
                              choices=[("beef", "Beef"),
                                       ("pork", "Pork")])


class HistoryPlot(panels.Plot):
    width = 600
    height = 400
    name = "History"

    def plot(self, inputs):
        #import pdb; pdb.set_trace()
        p = ggplot(meat, aes(x='date', y=inputs.yvar))
        if inputs.smoother:
            p = p + stat_smooth(color="red")
        p = p + geom_point() + ggtitle(inputs.title)
        return p


class ScatterPlot(panels.Plot):
    width = 600
    height = 400
    name = "Scatter"

    def plot(self, inputs):
        p = ggplot(meat, aes(x='date', y=inputs.yvar))
        if inputs.smoother:
            p = p + stat_smooth(color="blue")
        p = p + geom_point() + ggtitle(inputs.title)
        return p

     
class TabPanel(panels.Tabs):
    tabs = [HistoryPlot(), ScatterPlot()]


class MyGleam(Page):
    title = "Meat Scatter Plot"
    input = GleamInput()
    output = TabPanel()


app = Flask('myapp')
MyGleam.add_flask(app)
if __name__ == "__main__":
    app.debug = True
    app.run()
