#! /usr/bin/python
import sys

from gm_custom import git_push_remotes

argc = len(sys.argv)
if argc < 3:
    print
    print 'Push a repo to multiple remotes'
    print
    print '      Usage: gm-pr project_name remote_names'
    print '         Ex: gm-pr kortex local github borg'
    print
    sys.exit(0)

repo_name   = sys.argv[1]
remote_list = sys.argv[2:argc]

git_push_remotes( repo_name, remote_list, 'master' )


