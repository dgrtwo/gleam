from flask import Flask
import gleam
from gleam import widgets, outputs
from wtforms import fields

from ggplot import meat, aes, stat_smooth, geom_point, ggtitle

class MyGleam(gleam.Page):
    pageTitle = "Meat Scatter Plot"

    # xvar = widgets.Select(label="X axis", choices=["Date"])
    smoother = fields.BooleanField(label="Add Smoothing Curve?")
    title = fields.StringField(label="Title of plot:")
    yvar = fields.SelectField(label="Y axis",
                              choices=[("beef", "Beef"),
                                       ("pork", "Pork")])

    @outputs.Plot(width=600, height=400, plotter='ggplot')
    def scatter_plot(smoother, title, yvar):
        # p = ggplot(meat, aes(x=xvar, y=yvar))
        p = ggplot(meat, aes(x='date', y=yvar))
        if smoother:
            p = p + stat_smooth(color="red")

        return p + geom_point() + ggtitle(title)

app = Flask('myapp')
MyGleam.add_flask(app)
if __name__ == "__main__":
    app.debug = True
    app.run()

    # MyGleam.run(host='0.0.0.0', port=80)
