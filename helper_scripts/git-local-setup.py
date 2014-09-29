#! /usr/bin/env python
import os, sys, string, math
import commands

sys.path.append(os.path.abspath(os.getenv('HOME')+"/src/python/git_manager/"))
sys.path.append(os.path.abspath(os.getenv('HOME')+"/src/python/git_manager/helper_scripts/"))
from gm_resources import *
from utility      import *
from gm_custom    import *

local_git_dir= get_home()+'/gitrepos/'


if len(sys.argv) == 2:
    repo_name=sys.argv[1]
    repo_path=get_repository_path(repo_name)
    if not is_valid_dir(repo_path):
        print
        print 'no such directory exists ['+repo_path+']'
        print
        sys.exit(1)
elif is_valid_dir(get_pwd()+'/.git'):
    repo_path = get_pwd()
    print
    print 'running inside a git repo ['+repo_path+']'
    print
    repo_name = os.path.basename(get_pwd())
else:
    print 'either run inside a repo folder or provide the name of the repo'
    print 'usage: ' + sys.argv[0] + ' repository_name'
    sys.exit(1)


full_local_path=local_git_dir+repo_name+'.git'

print 'repo_name        : [ '+repo_name.ljust(40)+']'
print 'repo_path        : [ '+repo_path.ljust(40)+']'
print 'full_local_path  : [ '+full_local_path.ljust(40)+']'
print

g = generate_git_report( repo_name )

# init bare repo if it does not exist
if is_valid_dir(full_local_path) is False:
    print 'running on local:'
    print ''
    print '   mkdir -p '+full_local_path
    run_command( 'mkdir -p '+full_local_path )
    print '   cd '+full_local_path
    os.chdir( full_local_path )
    print '   git --bare init'
    run_command( 'git --bare init' )
    print '   setup done'
    os.chdir( repo_path )
    print ''
else:
    print '- local repo exists [ '+full_local_path+' ]'

# add local as remote if it does not exist
if 'local' not in g.remotes:
    print 'running: git remote add local '+full_local_path
    run_command('git remote add local '+full_local_path)
    print
else:
    print '- local remote exists'

print '     push local'
print '     running: git push local master'
run_command('git push local master')

remotes, rsymbols = get_remote_names()
# print remotes

# installing remotes if they are mounted
remote_ops=False
for remote in remotes:
    mount_point = get_mount_point( remote )
    if len(mount_point) == 0:
        continue
    print 'REMOTE ['+remote+']'
    remote_path = generate_remote_path( remote, repo_name )
    if is_valid_dir( remote_path ) is False:
        print '    copying local git repo to the remote'
        print '    running \'cp -r '+full_local_path+' '+mount_point+'/backup/gitrepos/\''
        run_command('cp -r '+full_local_path+' '+mount_point+'/backup/gitrepos/')

    if remote not in g.remotes:
        print '    running \'git remote add '+remote+' '+remote_path+'\''
        run_command('git remote add '+remote+' '+remote_path)

    print '    running push'
    run_command( 'git push '+remote+' master' )
    remote_ops=True

if not remote_ops:
    print '- no external remote detected'

print









