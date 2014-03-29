from flask import Flask
import gleam
from gleam import widgets, outputs

import numpy as np
import matplotlib
import pylab as plt
import pandas as pd

df = pd.DataFrame(dict(x=np.random.randn(1000),
                    y=np.random.randn(1000)))
print 'regenerating!'

class MyGleam(gleam.Page):
    Title = "Meat Scatter Plot"

    # xvar = widgets.Select(label="X axis", choices=["Date"])
    yvar = widgets.Select(label="Y axis", choices=["beef", "pork"])
    grid = widgets.Checkbox(label="Show grid")
    title = widgets.Text(label="Title of plot:")

    @outputs.Plot(width=600, height=400)
    def scatter_plot_matplotlib(grid, title, yvar):
        plt.scatter(df['x'], df['y'])
        print df['x'].head()
        if grid:
            plt.grid()

        # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
        # ax1 = plt.subplot(1,2,1)
        # ax1.set_title(title)
        # ax1.hist2d(df['x'], df['y'])

app = Flask('myapp')
MyGleam.add_flask(app)
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
