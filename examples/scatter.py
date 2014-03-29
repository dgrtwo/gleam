import gleam
from gleam import widgets, outputs

from ggplot import *


class MyGleam(gleam.Page):
    Title = "Meat Scatter Plot"

    xvar = widgets.Select(label="X axis", choices=["Date"])
    yvar = widgets.Select(label="Y axis", choices=["beef", "pork"])
    smoother = widgets.Checkbox(label="Add Smoothing Curve?")
    title = widgets.Text(label="Title of plot:")

    @outputs.Plot(width=600, height=400)
    def scatter_plot(xvar, yvar, smoother):
        p = ggplot(meat, aes(x=xvar, y=yvar))
        if smoother:
            p = p + stat_smooth()

        print p + geom_point() + ggtitle(title)


if __name__ == "__main__":
    MyGleam.run()
