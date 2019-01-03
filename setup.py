#!/usr/bin/env python

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and data files required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

from distutils.core import setup


setup(name="pynea",
      version="1.0.0",
      description="""Pynea facilitates the reproducibility of LaTeX documents by embedding
                     the scripts and data files required to regenerate the figures within
                     the document itself.""",
      author="Christian Thomas Jacobs",
      author_email="christian@christianjacobs.uk",
      packages=["pynea"],
      package_dir={"pynea": "pynea"},
      scripts=["bin/pynea"],
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
      ]
      )
