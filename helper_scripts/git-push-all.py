#! /usr/bin/env python

import os, sys, string, math
import commands

# from gm_resources import *
from gm_custom    import *

sys.path.append(os.path.abspath(os.getenv('HOME')+"/src/python/git_manager/helper_scripts/"))

if len(sys.argv) != 2:
    print 'usage: ' + sys.argv[0] + ' remote_name'
    sys.exit(1)

remote_name = sys.argv[1]

repos = get_repositories()

smsg = ""
for repo in repos:
    if repo == "":
        continue

    rfolder = get_repository_path( repo )

    g = generate_git_report( repo )
    if g.isrepo == -1:
        smsg += '    skipped [' + repo + '] - not a git repo\n'
        continue
    if is_valid_repo_dir( repo ) is False:
        smsg += '    skipped [' + repo + '] - not a valid directory\n'
        continue

    os.chdir( rfolder )
    cmd = 'git push '+ remote_name + ' master'
    print repo.ljust(25) + ' -> ' + cmd
    rc, git_st = commands.getstatusoutput(cmd)
    if rc != 0:
        smsg += '    failed  [' + repo + ']\n'


print '---------------------------------------------------------'
print smsg
