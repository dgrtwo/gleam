import os
from distutils.core import setup
setup(name="gleam",
      author="David Robinson",
      author_email="dgrtwo@princeton.edu",
      description="Interactive visualization in Python",
      version="0.1",
      packages=["gleam"],
      package_dir={"gleam": "src/gleam"},
      package_data={"gleam": [os.path.join("templates", "*"),
                              os.path.join("static", "*"),
                              os.path.join("static", "*", "*")]}
      )
