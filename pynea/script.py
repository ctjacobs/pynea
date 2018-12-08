#!/usr/bin/env python3

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and dependencies required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

from pynea.resource import Resource


class Script(Resource):

    """ A script used to produce a figure in the LaTeX document. """

    pass
