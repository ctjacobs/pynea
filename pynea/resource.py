#!/usr/bin/env python3

"""
Copyright (C) 2018 Christian Thomas Jacobs

Pynea facilitates the reproducibility of LaTeX documents by embedding the scripts and dependencies required to regenerate the figures within the document itself.

Pynea is released under the MIT license. See the file LICENSE.md for more details.
"""

import os.path
import git


class Resource(object):

    """ A generic resource, assumed to be located within a directory version controlled by Git. """

    def __init__(self, path):
        """ Set up the resource and record its path. """

        # The path to the resource.
        assert(os.path.exists(path))
        self.path = path

        return
    
    @property
    def is_modified(self):
        """ Return True if the resource is in the list of modified repository files or is untracked. Otherwise return False. """
        try:
            # Open the resource's Git repository.
            repo = git.Repo(self.path, search_parent_directories=True)
            # Get the path to the repository's root directory.
            root = repo.git.working_dir
            # Get the list of (tracked) modified files.
            modified = [os.path.join(root, f.a_path) for f in repo.index.diff(None)]
            # Get the list of untracked files.
            untracked = [os.path.join(root, f) for f in repo.untracked_files]
            # Check whether or not the resource is in the list of modified files or untracked files.
            return ((self.path in modified) or (self.path in untracked))
        except git.InvalidGitRepositoryError as e:
            # Not under version control, so assume modified.
            return True
        except git.exc.NoSuchPathError as e:
            # File does not exist and needs generating.
            return True
        
        return False

    @property
    def revision(self):
        """ Return the SHA hash of the Git repository's HEAD commit. """
        repo = git.Repo(self.path, search_parent_directories=True)
        sha = repo.head.object.hexsha
        return sha
