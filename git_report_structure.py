#! /usr/bin/python
import os, sys, string, re, commands

class GitReport:
    def __init__(self):
        self.repo_name = ''
        self.path      = ''
        self.isrepo    = -1
        self.commit    = -1
        self.wdc       = -1
        self.branch    = ''
        self.ufiles    = '' # untracked files
        self.cfiles    = '' # changed files
        self.sfiles    = '' # staged files
        self.remotes   = '' # remote repos
        self.lcdate    = '' # last commit date
        self.lcuser    = '' # last commit user
        self.lcmsg     = '' # last commit message
        self.lcrev     = '' # last commit revision id
        self.lcsyncrem = '' # last commit synced remotes
        self.raw_status  = ''
        self.raw_hist    = ''
        self.raw_remotes = ''

    def clear(self):
        self.isrepo    = -1
        self.commit    = -1
        self.wdc       = -1
        self.branch    = ''
        self.ufiles    = '' # untracked files
        self.cfiles    = '' # changed files
        self.sfiles    = '' # staged files
        self.remotes   = '' # remote repos
        self.lcdate    = '' # last commit date
        self.lcuser    = '' # last commit user
        self.lcmsg     = '' # last commit message
        self.lcrev     = '' # last commit revision id
        self.lcsyncrem = '' # last commit synced remotes
        self.raw_status  = ''
        self.raw_hist    = ''
        self.raw_remotes = ''

    def display(self):
        kwd_sz = 30
        print
        print 'name'.ljust(kwd_sz)+'['+ self.repo_name.rjust(kwd_sz) + ']'
        print 'path'.ljust(kwd_sz)+'['+ self.path.rjust(kwd_sz) + ']'
        print 'isrepo'.ljust(kwd_sz)+'['+ str(self.isrepo).rjust(kwd_sz) + ']'
        print 'branch'.ljust(kwd_sz)+'['+ self.branch.rjust(kwd_sz) + ']'
        if self.commit == 1:
            print 'commit'.ljust(kwd_sz)+'['+ str('necessary').rjust(kwd_sz) + ']'
        else:
            print 'commit'.ljust(kwd_sz)+'['+ str('-').rjust(kwd_sz) + ']'
        print 'remotes'.ljust(kwd_sz)+'['+ str( len(self.remotes) ).rjust(kwd_sz) + ']', self.remotes

        if self.wdc == 0:
            print 'workdir'.ljust(kwd_sz)+'['+'clean'.rjust(kwd_sz)+']'
        else:
            print 'workdir'.ljust(kwd_sz)+'['+'dirty'.rjust(kwd_sz)+']'
        print 'Staged'.ljust(kwd_sz) + '[' + str( len(self.sfiles) ).rjust(kwd_sz) + ']', self.sfiles
        print 'Changed'.ljust(kwd_sz) + '[' + str( len(self.cfiles) ).rjust(kwd_sz) + ']', self.cfiles
        print 'Untracked'.ljust(kwd_sz) + '[' + str( len(self.ufiles) ).rjust(kwd_sz) + ']', self.ufiles
        print 'Last Commit'.ljust(kwd_sz) + '[ ' + self.lcdate + ' ' + self.lcmsg + ' ' + ']',  self.lcsyncrem
        print

    def parse_last_commit_history( self ):
        rc, git_hists = commands.getstatusoutput('git log --pretty=format:\"%h %ad | %s%d [%an]\" --graph --date=short --max-count=10')
        self.raw_hist = git_hists
        if rc != 0:
            return
        git_hists = re.sub(r'\x1b[^m]*m','',git_hists)
        last_commit = git_hists.splitlines()[0].strip()
        regps = re.match( r'(.*)\|(.*)\((.*)\)(.*)', last_commit, re.M)
        if regps:
            self.lcrev     = regps.group(1).strip().split(' ')[0]
            self.lcdate    = regps.group(1).strip().split(' ')[1]
            self.lcmsg     = regps.group(2).strip()
            self.lcsyncrem = [ f.strip() for f in filter(None, regps.group(3).strip().replace('/'+self.branch,'').split(',')) ]
            self.lcuser    = regps.group(4).strip().replace('[','').replace(']','')

    def parse_remote( self ):
        if self.path == '':
            print 'path not set'
            return
        os.chdir( self.path )
        rc, self.raw_remotes = commands.getstatusoutput('git remote')
        if rc == 0:
            self.remotes = self.raw_remotes.splitlines()
            # re.split( '\n', raw_remotes )

    def parse_status( self ):
        if self.path == '':
            print 'path not set'
            return
        os.chdir( self.path )
        rc, report = commands.getstatusoutput('git status')
        self.raw_status = report
        if rc != 0:
            return

        if report.find('Not a git repository') != -1:
            self.isrepo = 0
        else:
            self.isrepo = 1
        if report.find('branch') != -1:
            reout = re.search(r'branch (.*)',report)
            if reout:
                self.branch = reout.group(1)

        if report.find('working directory clean') != -1:
            self.wdc = 0
        else :
            if report.find('Untracked files:') != -1:
                # if this is not an initial commit following should return something
                reout = re.split( '(nothing added to commit but untracked files present).*', report, re.M)
                ufiles = reout[0]
                reout = re.split( '(no changes added to commit).*', ufiles, re.M)
                ufiles = reout[0]
                # get to te relevant section
                reout = re.split( '(Untracked files:).*', ufiles, re.M)
                ufiles = reout[2]
                reout = re.split( '(what will be committed\)).*', ufiles, re.M)
                ufiles = re.sub(r'\x1b[^m]*m','',reout[2])
                ufiles = re.split( '\n', ufiles )
                ufiles = filter( None, ufiles )
                self.ufiles = [ f.replace('\t', '') for f in ufiles]

            if report.find('Changes not staged for commit:') != -1:
                # if this is not an initial commit following should return something
                reout = re.split( '(nothing added to commit but untracked files present).*', report, re.M)
                cfiles = reout[0]
                reout = re.split( '(no changes added to commit).*', cfiles, re.M)
                cfiles = reout[0]
                reout = re.split( '(Untracked files:).*', cfiles, re.M)
                cfiles = reout[0]
                # get to te relevant section
                reout = re.split( '(Changes not staged for commit:).*', cfiles, re.M)
                cfiles = reout[2]
                reout = re.split( '(discard changes in working directory\)).*', cfiles, re.M)
                cfiles = re.sub(r'\x1b[^m]*m','',reout[2])
                cfiles = re.split( '\n', cfiles )
                cfiles = filter( None, cfiles )
                cfiles = [ f.replace('\t', '') for f in cfiles]
                self.cfiles = [ f.replace('modified:', '').strip() for f in cfiles]

            if report.find('Changes to be committed:') != -1:
                # if this is not an initial commit following should return something
                reout = re.split( '(nothing added to commit but untracked files present).*', report, re.M)
                sfiles = reout[0]
                reout = re.split( '(no changes added to commit).*', sfiles, re.M)
                sfiles = reout[0]
                reout = re.split( '(Untracked files:).*', sfiles, re.M)
                sfiles = reout[0]
                reout = re.split( '(Unmerged paths:).*', report, re.M)
                sfiles = reout[0]
                reout = re.split( '(Changes not staged for commit:).*', sfiles, re.M)
                sfiles = reout[0]
                # get to te relevant section
                reout = re.split( '(Changes to be committed:).*', sfiles, re.M)
                sfiles = reout[2]
                if sfiles.find( '..." to unstage\)' ) != -1:
                    reout = re.split( '(..." to unstage\)).*', sfiles, re.M)
                    sfiles = reout[2]

                sfiles = re.sub(r'\x1b[^m]*m','',reout[2])
                sfiles = re.split( '\n', sfiles )
                sfiles = filter( None, sfiles )
                sfiles = [ f.replace('\t', '') for f in sfiles]
                sfiles = [ f.replace('new file:', '').strip() for f in sfiles]
                self.sfiles = [ f.replace('modified:', '').strip() for f in sfiles]

            if report.find('Unmerged paths:') != -1:
                # if this is not an initial commit following should return something
                reout = re.split( '(nothing added to commit but untracked files present).*', report, re.M)
                sfiles = reout[0]
                reout = re.split( '(no changes added to commit).*', sfiles, re.M)
                sfiles = reout[0]
                reout = re.split( '(Untracked files:).*', sfiles, re.M)
                sfiles = reout[0]
                reout = re.split( '(Changes not staged for commit:).*', sfiles, re.M)
                sfiles = reout[0]
                reout = re.split( '(Unmerged paths:).*', sfiles, re.M)
                sfiles = reout[0]
                # get to te relevant section
                reout = re.split( '(Changes to be committed:).*', sfiles, re.M)
                sfiles = reout[2]
                if sfiles.find( '..." to unstage\)' ) != -1:
                    reout = re.split( '(..." to unstage\)).*', sfiles, re.M)
                    sfiles = reout[2]

                sfiles = re.sub(r'\x1b[^m]*m','',reout[2])
                sfiles = re.split( '\n', sfiles )
                sfiles = filter( None, sfiles )
                sfiles = [ f.replace('\t', '') for f in sfiles]
                sfiles = [ f.replace('new file:', '').strip() for f in sfiles]
                sfiles = [ f.replace('modified:', '').strip() for f in sfiles]
                sfiles = [ f.replace('both modified:', '').strip() for f in sfiles]
                self.sfiles += sfiles

        if len( self.sfiles ) + len( self.cfiles ) != 0 :
            self.commit = 1
        else :
            self.commit = 0

