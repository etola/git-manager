#! /usr/bin/env python

from utility import get_folders, get_home

def get_repositories():
    rep_names = [ "kortex",
              "kortex-ext-advanced",
              "kortex-ext-3d",
              "kortex-ext-calibration",
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

    rep_names.extend( [ "" ] )
    app_extra_names = get_folders( get_home() + '/src/cpp/applications-beta' );
    rep_names.extend( app_extra_names )

    # rep_names.extend( [ "", "color-to-gray", "skanner", "levmar"] )
    rep_names.extend( [ "", "shellscripts" ] )
    rep_names.extend( [ "", "git_manager" ] )
    rep_names.extend( [ "", "makefile-heaven" ] )

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
                'borg',
                'cruzer',
                'github',
                'echelon',
                'enterprise',
                'pegasus' ]

    remote_symbols = [ 'H', 'L', 'B', 'C', 'G', 'E', 'N', 'P' ]

    return remotes, remote_symbols
