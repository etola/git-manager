#! /usr/bin/env python
import os, sys, string, math, commands
from gm_custom import *

def rep_state( rname, rlist, tval ):
    if rname in rlist:
        return tval
    else:
        return '.'

def var_state( var ):
    if var:
        return '+'
    else:
        return ' '

def num_list_elem( l, n_just ):
    lsz = len(l)
    if lsz == 0:
        return '.'.rjust(n_just)
    else:
        return str(lsz).rjust(n_just)

def repo_remote_state( g ):
    msg =  ''
    remotes, remote_symbols = get_remote_names()
    cnt = 0
    for remote in remotes:
        rsymbol = remote_symbols[cnt]
        msg += rep_state( remote, g.lcsyncrem, rsymbol )
        cnt += 1
    return msg

remotes, remote_symbols = get_remote_names()
remote_header = ''
for rsym in remote_symbols:
    remote_header += rsym

print
print 'repository_name'.rjust(31) + ' |C| '+remote_header+' |' + 'Branch'.rjust(7) + ' |' + 'S'.rjust(2) + 'C'.rjust(2) + 'U'.rjust(3)
print '  ------------------------------------------------------------'

smsg = ''
msg  = ''

cnt = 0

repos = get_repositories()

for repo in repos:
    if repo == "":
        msg += '  ------------------------------------------------------------\n'
        continue
    g = generate_git_report( repo )
    if g.isrepo == -1:
        smsg += '    skipped ['+repo+'] - not a git repo\n'
        continue

    msg += '  [' + str( repos.index(repo)  ).rjust(2)  + ']'
    msg += g.repo_name.rjust(25) + ' |' + var_state(g.commit) + '| '
    msg += repo_remote_state( g )
    msg += ' |'
    msg += g.branch.rjust(7) + ' |'
    msg += num_list_elem(g.sfiles,2)
    msg += num_list_elem(g.cfiles,2)
    msg += num_list_elem(g.ufiles,3)
    if repo != repos[ len(repos)-1 ]:
        msg += '\n'

    cnt += 1

print msg
print '  ------------------------------------------------------------'

remotes, remote_symbols = get_remote_names()
cnt = 0
msg = '    '
for remote in remotes:
    rsymbol = remote_symbols[cnt]
    msg += (rsymbol+': '+remote).ljust(15)
    cnt += 1
    if cnt%4 == 0 and ( cnt != len(remotes) ):
        msg += '\n    '
print msg
print '  ------------------------------------------------------------'
print '      S : staged     C : changed   U : untracked'

if smsg :
    print '  ------------------------------------------------------------'
    print '  Skipped Repos'
    print smsg
