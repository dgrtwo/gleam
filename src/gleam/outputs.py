"""
Outputs are displayed to the user, such as figures or tables
"""

import os
import hashlib
import inspect


class Output:
    """An output displayed to the user"""
    def setup(self, name, env):
        """todo"""
        self.name = name
        self.values["name"] = name
        template = env.get_template(self.Template)
        self.rendered = template.render(**self.values)        


class Plot(Output):
    """A displayed figure"""
    Template = "plot.html"

    def __init__(self, width=600, height=600, plotter="matplotlib",
                 extension="png"):
        # to do: specify one not other
        self.values = {"height": height, "width": width}
        self.plotter = plotter
        self.extension = extension

    def __call__(self, func):
        """Using as a decorator"""
        self.func = func
        self.args = inspect.getargspec(func).args
        return self

    def setup(self, name, env):
        """create an output folder if it doesn't exist"""
        self.plot_dir = os.path.join("static", "figures", name)
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)
        Output.setup(self, name, env)

    def refresh(self, *args, **kwargs):
        # before
        h = hashlib.md5(str(args) + str(kwargs)).hexdigest()

        outfile = os.path.join(self.plot_dir, h + "." + self.extension)

        if os.path.exists(outfile):
            return {"src": outfile.replace("\/", "/")}

        if self.plotter == "custom":
            kwargs["__outfile"] = outfile

        if self.plotter == "matplotlib":
            from matplotlib import pyplot as plt
            plt.clf()

        ret = self.func(*args, **kwargs)

        # after
        if self.plotter == "matplotlib":
            plt.savefig(outfile)
        elif self.plotter == "ggplot":
            from ggplot.utils import ggsave
            ggsave(outfile, ret)
        return {"src": outfile.replace("\/", "/")}

    def __repr__(self):
        return self.rendered
