#! /usr/bin/env python

from utility import get_folders, get_home

def get_repositories():
    rep_names = [ "kortex",
              "kortex-ext-advanced",
              "kortex-ext-opencv",
              "cosmos",
              "karpet",
              "kutility",
              "argus",
              "margus",
              ""
    ]

    app_names = get_folders( get_home() + '/src/cpp/applications')
    rep_names.extend( app_names )

    # rep_names.extend( [ "" ] )
    # app_extra_names = get_folders( get_home() + '/src/cpp/applications-test' );
    # rep_names.extend( app_extra_names )

    # rep_names.extend( [ "", "color-to-gray", "skanner", "levmar"] )
    rep_names.extend( [ "", "shellscripts", "git_manager", "makefile-heaven" ] )
    # rep_names.extend( [ "makefile-heaven" ] )

    rep_names.extend( [ "", "applications-test" ] )

    return rep_names

def get_repositories_search_dirs():
    homedir = get_home()
    search_paths = [ homedir + '/src/cpp/lib/',
                     homedir + '/src/cpp/applications/',
                     homedir + '/src/cpp/applications-beta/',
                     homedir + '/src/python/',
                     homedir + '/src/cpp/',
                     homedir + '/src/' ]
    return search_paths

def get_remote_names():
    remotes = [ 'HEAD',
                'local',
                'arctic',
                'antarctic',
                'borg',
                'cruzer',
                'github',
                'echelon',
                'pegasus',
                'vault' ]

    remote_symbols = [ 'H', 'L', 'A', 'N', 'B', 'C', 'G', 'E', 'P', 'V' ]

    return remotes, remote_symbols
