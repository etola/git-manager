#! /usr/bin/python
import os, sys, commands

def get_folders(root_dir):
    folders = [ name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name)) ]
    return folders

def get_files(root_dir):
    files = [ name for name in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, name)) ]
    return files

def get_home():
    return os.path.abspath(os.getenv('HOME'))

def get_pwd():
    return os.path.abspath(os.getenv('PWD'))

def is_valid_dir( path ):
    return os.path.isdir( path )

def is_valid_file( path ):
    return os.path.isfile( path )

def run_command( cmd ):
    rc, cmd_info = commands.getstatusoutput(cmd)
    if rc != 0:
        print 'error processing command ['+cmd+']'
        print 'msg: '
        print cmd_info
        return rc, cmd_info

def get_mount_point( disk_name ):

    rc, cmd_info = commands.getstatusoutput( 'mount | grep -w '+disk_name )
    if len(cmd_info) == 0:
        return ''
    else:
        rc, mount_dir = commands.getstatusoutput('echo \''+cmd_info+'\' | awk \'{print $3}\'')
        if rc != 0:
            print 'error processing command!'
            print mount_dir
        return mount_dir



