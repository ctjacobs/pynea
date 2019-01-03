#!/usr/bin/env python3

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and data files required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

from TexSoup import TexSoup
import os.path

from pynea.figure import Figure
from pynea.script import Script
from pynea.data import Data


class Parser:

    """ Parses the LaTeX document and extracts the relevant PDF figures and associated Pynea commands. """

    def __init__(self):
        return
        
    def read(self, path):
        """ Read the .tex file and return a list of Figure objects that represent each figure included in the .tex file,
        and include the paths to the script and the data files that each figure relies on. """
        figures = []
    
        with open(path, "r") as f:
            tex = TexSoup(f)

            # Find all figure environments.
            found = list(tex.find_all("figure"))

            # Loop over all figures in the document.
            for f in found:

                # Get the path to the figure.
                path = os.path.abspath(os.path.join(os.path.dirname(path), f.includegraphics.args[-1]))
                
                # Only consider PDF figures.
                if(path.split(".")[-1] != "pdf"):
                    continue
                
                # Parse the remaining Pynea parameters.
                try:
                    script = Script(os.path.abspath(f.pyneascript.args[0]))
                    command = f.pyneacommand.args[0]
                    data = [Data(os.path.abspath(d)) for d in f.pyneadata.args[0].split()]
                
                    figure = Figure(path, script, command, data)
                    figures.append(figure)
                except AttributeError as e:
                    print("Warning: No script, command and/or data files specified for figure %s. Skipping..." % (path))
                    continue

        return figures

