#! /usr/bin/python
import sys, os

sys.path.append(os.path.abspath(os.getenv('HOME')+"/src/python/git_manager/"))

from gm_core import *

if len(sys.argv) < 2:
    print
    print 'Usage: ' + sys.argv[0] + ' repo_name'
    print
    sys.exit(0)

raw_out = False
for arg in sys.argv:
    if arg == '--raw':
        raw_out = True

repo_name   = sys.argv[1]

if is_valid_repo_dir( repo_name ) is False:
    print 'could not find repo [ ' + repo_name + ' ]'
    sys.exit(1)

folder_path = get_repository_path( repo_name )

g = generate_git_report( repo_name )

if raw_out is False:
    g.display()
else :
    os.chdir( folder_path )
    print 'Remotes'
    print '--------------------------------------------------------------'
    # rc, git_st = commands.getstatusoutput('git remote -v')
    # print git_st
    print g.raw_remotes
    print

    print 'Short History'
    print '--------------------------------------------------------------'
    # rc, git_st = commands.getstatusoutput('git hists')
    # print git_st
    print g.raw_hist
    print

    print 'Status'
    print '--------------------------------------------------------------'
    # rc, git_st = commands.getstatusoutput('git st')
    # print git_st
    print g.raw_status
    print

    print 'Pushed Remotes'
    print '--------------------------------------------------------------'
    print g.lcsyncrem
    print
