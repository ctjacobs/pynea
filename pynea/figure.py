#!/usr/bin/env python3

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and dependencies required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

from subprocess import call
import fitz
import os.path
import git
import re

from pynea.resource import Resource


class Figure(Resource):

    """ A figure to be included in the LaTeX document. """

    def __init__(self, path, script, command, dependencies):
        """ Save the path to the figure file and resources used to generate it. """

        # The path to the figure file itself.
        self.path = path
        # The script that generated the figure.
        self.script = script
        # The command used to execute the script.
        self.command = command
        # Any data files, etc, that the script depends on.
        self.dependencies = dependencies    
        return
    
    @property
    def is_modified(self):
        """ Return True if the figure, script, dependencies and/or command has changed. """

        # Has the figure itself changed?
        figure_modified = super(Figure, self).is_modified
        if(not figure_modified):
            # Has the script which generated the figure changed?
            script_modified = self.script.is_modified
            if(not script_modified):
                # Have the script's dependencies changed?
                dependencies_modified = any([d.is_modified for d in self.dependencies])
                if(not dependencies_modified):
                    # Has the command used to run the script changed?
                    # Open figure and obtain the previously-used command from the metadata.      
                    pdf = fitz.open(self.path)
                    keywords = pdf.metadata["keywords"]
                    # NOTE: If the previously-used command is not found then it is assumed that the figure has been modified.
                    if(keywords):
                        m = re.match(r"script_command:(.+),", keywords)
                        if(m):
                            previous_command = m.group(1)
                            command_modified = (self.command != previous_command)
                            if(not command_modified):
                                return False

        return True
        
    def generate(self):
        """ Generate the figure by running the script which generates it. """

        # Record the current working directory.
        cwd = os.getcwd()
        # Change to the script's working directory.
        os.chdir(os.path.dirname(self.script.path))
        # Re-run the command.
        return_code = call(self.command, shell=True)
        # Switch back to the current working directory.
        os.chdir(cwd)
        return return_code
        
    def embed(self):
        """ Embed the script and dependencies in the figure. """

        # Open the PDF file that will host the script file and dependencies.
        pdf = fitz.open(self.path)
    
        # Embed script.
        b = open(self.script.path, "rb").read()
        try:
            pdf.embeddedFileUpd(self.script.path, b)
        except:
            pdf.embeddedFileAdd(b, self.script.path)
        pdf.save(pdf.name, incremental=True)
                
        # Embed dependencies (e.g. data files).
        for dependency in self.dependencies:
            b = open(dependency.path, "rb").read()
            try:
                pdf.embeddedFileUpd(dependency.path, b)
            except:
                pdf.embeddedFileAdd(b, dependency.path)
            pdf.save(pdf.name, incremental=True)
            
        # Embed metadata (including command used to run the script).
        metadata = pdf.metadata
        metadata["keywords"] = "script_command:%s, script_git_revision:%s" % (self.command, self.script.revision)
        pdf.setMetadata(metadata)
        pdf.save(pdf.name, incremental=True)
        
        # Close the figure.
        pdf.close()
        
        return
