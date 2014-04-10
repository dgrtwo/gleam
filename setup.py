import os
from setuptools import setup

setup(name="gleam",
      author="David Robinson",
      author_email="dgrtwo@princeton.edu",
      description="Interactive visualization in Python",
      version="0.1.2",
      packages=["gleam"],
      package_dir={"gleam": "src/gleam"},
      package_data={"gleam": [os.path.join("templates", "*"),
                              os.path.join("static", "*", "*")]},
      install_requires=['Flask', 'Jinja2', 'WTForms']
      )
