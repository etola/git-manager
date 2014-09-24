#! /usr/bin/env python
import os, sys, string, math

sys.path.append(os.path.abspath(os.getenv('HOME')+"/src/python/git_manager/"))

from git_report_structure import *
from gm_resources         import *
from utility              import *

def is_valid_repo_dir( repo_name ):
    rep_dir = get_repository_path( repo_name )
    return is_valid_dir( rep_dir )

def is_valid_remote( rname ):
    remotes, rsyms = get_remote_names()
    if rname in remotes:
        return True
    else :
        return False


def get_repository_path( repo_name ):

    search_paths = get_repositories_search_dirs()

    folder_path = repo_name
    for rp in search_paths:
        ppath = rp + repo_name
        if is_valid_dir( ppath ) is True:
            folder_path = ppath
            break
    return folder_path

def git_push_remotes( repo_name, remote_list, branch_name ):

    rep_path = get_repository_path( repo_name )

    os.chdir( rep_path )
    rc, git_st = commands.getstatusoutput('git st')
    if rc != 0:
        print 'could not find a repository at ['+rep_path+']'
        sys.exit(1)

    smsg = ''
    for remote in remote_list:

        if is_valid_remote( remote ) is False:
            smsg += 'skipping - not a valid remote ['+remote+']\n'
            continue

        cmd = 'git push '+ remote + ' ' + branch_name
        print repo_name + ' -> ' + cmd
        rc, git_st = commands.getstatusoutput(cmd)
        if rc != 0:
            print 'failed to push ['+remote+']'
            smsg += 'problem pushing'.ljust(40) +  ': ' + repo + '\n'
            print git_st

    print '---------------------------------------------------------'
    print smsg


def git_push_projects( repo_names, branch_name, remote_name ):

    smsg = ''

    for repo in repo_names:
        repo_path = get_repository_path( repo )

        if is_valid_repo_dir( repo_path ) is False:
            smsg += 'skipping push - not a valid directory'.ljust(40) + ': ' + repo + '\n'
            continue

        os.chdir( repo_path )
        cmd = 'git push ' + remote_name + ' ' + branch_name
        print  repo.ljust(24) + ' -> ' + cmd

        g = generate_git_report( repo )

        if g.isrepo == -1:
            smsg += 'skipping push - could not find'.ljust(40) + ': ' + repo + '\n'
            sys.exit(1)
        if g.commit == 1:
            smsg += 'skipping push - dirty commit'.ljust(40) + ': ' + repo + '\n'
            continue

        rc, git_staus = commands.getstatusoutput(cmd)
        if rc != 0:
            smsg += 'problem pushing'.ljust(40) +  ': ' + repo + '\n'
            print git_staus
            continue

    print '---------------------------------------------------------'
    print smsg

def generate_git_report( repo_name ):
    if is_valid_repo_dir( repo_name ) is False:
        return None

    g = GitReport()
    g.repo_name = repo_name
    g.path = get_repository_path( repo_name )
    g.parse_status()
    g.parse_remote()
    g.parse_last_commit_history()
    return g

def generate_remote_path( remote_name, repo_name ):
    return get_mount_point(remote_name)+'/backup/gitrepos/'+repo_name+'.git'
