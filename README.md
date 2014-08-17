git-manager
===========

An interactive command line interface for displaying the state of multiple git
repositories in a single screen

- This scripts are for managing multiple git repositories from command line. It
checks the state of 'push'es to remotes and reports the up-to-date'ness of them.

- It also displays detailed raw output for repositories if there's enough screen
space. Otherwise, you can display detail repo information by switching the
display mode of the manager.

- Also, support for performing simple git operations on the repos, singly or in a
batch manner will be implemented soon.

- Adding and Removing repositories to track (editing of the .gmconfig file) will
  be made through the interface in future versions


file explanation
================

git-manager-gui.py : interactive manager - curses based

.gmconfig          : git manager gui is now configured through the ~/.gmconfig file.

                     - Adding a Repository:
                        you can add your repos by adding entries like
                        repo[kortex][/home/tola/src/cpp/lib/kortex]
                        repo[KX-OCV][/home/tola/src/cpp/lib/kortex-ext-opencv]

                        not found git repos will be skipped

                     - Defining a remote:
                       you can define remote names and symbols as:
                         remote[HEAD][H]
                         remote[borg][B]
                         remote[local][L]

                       symbols need to be single letters but it is not checked
                       in this version...


some tips:
==========

- To display the keybindings, press 'l'

- Repository information is cached once the application is started. To update it,
  press 'u'


Some Example Screenshots:
=========================

Full Screen View (Enough space in screen to display detailed info for repo):
![Alt text](/imgs/gmscreenshot.png?raw=true "Screenshot for Full Screen Mode")

Legend Overlay:
![Alt text](/imgs/gm-legend.png?raw=true "Legend Overlay")

Only Summary View is displayed if not enough space is available:
![Alt text](/imgs/gm-master-view.png?raw=true "Single View")
