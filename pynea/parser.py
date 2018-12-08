#!/usr/bin/env python3

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and dependencies required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

from TexSoup import TexSoup
import os.path

from pynea.figure import Figure
from pynea.script import Script
from pynea.dependency import Dependency


class Parser:

    """ Parses the LaTeX document and extracts the relevant PDF figures and associated Pynea commands. """

    def __init__(self):
        return
        
    def read(self, path):
        """ Read the .tex file and return a list of Figure objects that represent each figure included in the .tex file,
        and include the paths to the script and the dependencies that each figure relies on. """
        figures = []
    
        with open(path, "r") as f:
            tex = TexSoup(f)
            # Loop over all figures in the document.
            for figure in tex.figure:
                # Get the path to the figure.
                path = os.path.abspath(figure.includegraphics.args[-1])
                
                # Only consider PDF figures.
                if(path.split(".")[-1] != "pdf"):
                    continue
                
                # Parse the remaining Pynea parameters.
                script = Script(os.path.abspath(figure.pyneascript.args[0]))
                command = figure.pyneacommand.args[0]
                dependencies = [Dependency(os.path.abspath(d)) for d in figure.pyneadependencies.args[0].split()]
                
                figure = Figure(path, script, command, dependencies)
                figures.append(figure)
    
        return figures

