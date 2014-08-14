#! /usr/bin/python
import os, sys, commands

def get_folders(root_dir):
    folders = [ name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name)) ]
    return folders

def get_home():
    return os.path.abspath(os.getenv('HOME'))

def is_valid_dir( path ):
    return os.path.isdir( path )

