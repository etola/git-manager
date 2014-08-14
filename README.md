git-manager
===========

An interactive command line interface for displaying the state of multiple git
repositories in a single screen

This scripts are for managing multiple git repositories from command line. It
checks the state of 'push'es to remotes and reports the up-to-date'ness of them.

It also displays detailed raw output for repositories if there's enough screen
space. Otherwise, you can display detail repo information by switching the
display mode of the manager.

Also, support for performing simple git operations on the repos, singly or in a
batch manner will be implemented soon.


file explanation
================

git-manager-gui.py : interactive manager - curses based

git-manager.py     : just reports the current state and exits - no curses, no interaction

gm_resources.py : this is the file the repositories and the search directories
                  to find these repos are defined. You need to modify these
                  scripts for your own uses.



Some Example Screenshots:

![Alt text](/imgs/gmscreenshot.png?raw=true "Screenshot for Full Screen Mode")


