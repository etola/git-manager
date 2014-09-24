#! /usr/bin/python
import sys

from gm_custom import *

argc = len(sys.argv)
if argc < 3:
    print
    print 'Push multiple projects to a single remote'
    print
    print '      Usage: gm-pp remote_name repo_names'
    print '         Ex: gm-pp borg kortex kortex-ext-3d blender'
    print
    sys.exit(0)

remote_name = sys.argv[1]
repo_names  = sys.argv[2:argc]

if is_valid_remote( remote_name ) is False:
    print 'Not a valid remote name ['+remote_name+']'
    sys.exit(1)

git_push_projects( repo_names, 'master', remote_name )

