"""
Outputs are displayed to the user, such as figures or tables
"""

import os
import hashlib
import inspect


class Output:
    """An output displayed to the user"""
    def setup(self):
        """by default, nothing happens in setup"""
        pass


class Plot(Output):
    """A displayed figure"""
    def __init__(self, width=600, height=600, type="matplotlib",
                 extension="pdf"):
        # to do: specify one not other
        self.width = width
        self.height = height
        self.type = type
        self.extension = extension

    def __call__(self, func):
        """Using as a decorator"""
        self.func = func
        self.args = inspect.getargspec(func).args
        return self

    def setup(self, name):
        """create an output folder if it doesn't exist"""
        self.name = name
        self.plot_dir = os.path.join("static", "figures", name)
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)

    def refresh(self, *args, **kwargs):
        # before
        h = hashlib.md5(str(args) + str(kwargs)).hexdigest()

        outfile = os.path.join(self.plot_dir, h + "." + self.extension)

        if type == "custom":
            kwargs["__outfile"] = outfile

        ret = self.func(*args, **kwargs)

        # after
        if type == "matplotlib":
            from matplotlib import pyplot as plt
            plt.save(outfile)
        elif type == "ggplot":
            from ggplot.utils import ggsave
            ggsave(outfile)
        return {"src": outfile.replace("\/", "/")}
