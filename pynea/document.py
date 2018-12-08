#!/usr/bin/env python3

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and dependencies required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

import fitz
import os.path
from subprocess import call

from pynea.parser import Parser


class Document:

    """ The LaTeX document which includes a set of PDF figures. """

    def __init__(self, tex):
        """ Record the .tex file's path and parse it to locate all the figures to be included. """

        # Path to LaTeX source.
        self.path = tex
    
        # Parse .tex file for all PDF figures.
        p = Parser()
        self.figures = p.read(self.path)
        
        return
        
    def compile(self):
        """ Compile the LaTeX document as a PDF. """

        # Record the current working directory.
        cwd = os.getcwd()
        # Change to the LaTeX documents's working directory.
        os.chdir(os.path.dirname(self.path))
        # Call pdflatex.
        return_code = call("pdflatex %s" % (self.path), shell=True) 
        # Switch back to the current working directory.
        os.chdir(cwd)
        
        return return_code
        
    def embed(self):
        """ Embed each figure within the compiled document. """

        # Open the PDF file that will host the source file.
        pdf = fitz.open(self.path[:-4]+".pdf")
    
        # Embed figure files.
        for figure in self.figures:
            working_directory = "./"
            b = open(os.path.join(working_directory, figure.path), "rb").read()
            try:
                pdf.embeddedFileUpd(figure.path, b)
            except:
                pdf.embeddedFileAdd(b, figure.path)
            pdf.save(pdf.name, incremental=True)
                
        pdf.close()
        
        return
