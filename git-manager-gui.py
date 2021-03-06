#! /usr/bin/env python

import sys, os, curses, re, math

from git_report_structure import *
from utility              import *

CONFIG_FILE = get_home() + '/.gmconfig'

class Layout:
    def __init__(self):
        self.xs  = 0      # screen coordinates
        self.ys  = 0
        self.xe  = 0
        self.ye  = 0
        self.x0  = 0      # starting coordinates for the pad
        self.y0  = 0

    def update_screen_coords( self, ys, ye, xs, xe ):
        self.xs = xs
        self.ys = ys
        self.xe = xe
        self.ye = ye

    def refresh( self, pad ):
        pad.refresh( self.y0, self.x0, self.ys, self.xs, self.ye, self.xe )

    def erase( self ):
        tmp_pad = curses.newpad( self.ye-self.ys+1, self.xe-self.xs+1 )
        tmp_pad.refresh( 0, 0, self.ys, self.xs, self.ye, self.xe )

    def h( self ):
        return self.ye-self.ys+1

    def w( self ):
        return self.xe-self.xs+1


def num_list_elem( l ):
    lsz = len(l)
    if lsz == 0:
        return '.'
    else:
        return str(lsz)

def var_state( var ):
    if var:
        return '+'
    else:
        return ' '

def rep_state( rname, rlist, tval ):
    if rname in rlist:
        return tval
    else:
        return '.'

def repo_remote_state( g ):
    msg =  ''
    cnt = 0
    for remote in remotes:
        rsymbol = remote_symbols[cnt]
        msg += rep_state( remote, g.lcsyncrem, rsymbol )
        cnt += 1
    return msg

def add_new_repo( scr ):
    global msg_pad
    curses.echo()
    h,w=scr.getmaxyx()

    scr.hline( h-2, 0, curses.ACS_HLINE, w, curses.color_pair(5) )
    scr.addstr( h-1, 0, 'repo-name: ',  curses.color_pair(2) )

    rname = scr.getstr(h-1,11,20)

    cname = re.sub( r'[^A-Za-z \-]', '', rname )

    if rname != re.sub( r'[^A-Za-z \-]', '', rname ):
        msg_pad.addstr( 1, 0, 'cancelled input - not a valid name ['+rname+']', curses.color_pair(2) )
    else:
        if rname == '----':
            msg_pad.addstr( 1, 0, 'adding separator' )
            config_file_add_new_repo( '----', None )
            reload_repos()
        else:

            scr.addstr( h-1, len(rname)+12, 'repo-address: ~/',  curses.color_pair(2) )
            rpath = get_home() + '/' + scr.getstr(h-1,len(rname)+28,w-30-len(rname)) # Creates an "input box" at the location (0,1) with an input buffer of 15 chars

            if is_valid_dir(rpath) is True:
                msg_pad.addstr( 1, 0, 'added rule repo['+rname+']['+rpath+'] to the '+CONFIG_FILE, curses.A_STANDOUT );
                config_file_add_new_repo( rname, rpath )
                reload_repos()
            else:
                msg_pad.addstr( 1, 0, 'not a valid path ['+rpath+'] - not added', curses.color_pair(2) )

    curses.noecho()

def get_input( scr ):
    global msg_pad
    curses.echo()            # Allows out input to be echo'd to the screen

    # draw_content()
    # draw_main( scr )
    # scr.refresh()
    h,w=scr.getmaxyx()

    scr.hline( h-2, 0, curses.ACS_HLINE, w, curses.color_pair(5) )

    cmd = scr.getstr(h-1,1,15) # Creates an "input box" at the location (0,1) with an input buffer of 15 chars
    curses.noecho() # Turns echo back off

    msg_pad.addstr( 1, 0, cmd, curses.color_pair(2) )


def render_text( scr, text, y, x, h, w ):

    text = re.sub( r'\x1b[^m]*m','', text )
    text = text.splitlines()

    max_len = 0
    c = 0
    for st in text:
        lstr = len( st )
        if y+c >= h-2:
            break
        scr.addstr( y+c, x+3, st )
        if w <= (x+5+lstr):
            c = c + int( math.ceil((lstr+x+5)/float(w)) )
        else:
            c = c + 1
        max_len = max( max_len, lstr )

    y = y+c
    return y, max_len

def draw_repo_details( scr, g ):

    scr.erase()
    os.chdir( g.path )
    git_st = re.sub( r'\x1b[^m]*m', '', g.raw_hist )

    commits = git_st.splitlines()

    h,w = scr.getmaxyx()

    y = 0
    x = 1
    scr.vline(  y, 0, curses.ACS_VLINE, h     )

    scr.addstr( y,   x, ''.center(w-x),           curses.A_STANDOUT )
    scr.addstr( y+1, x, 'Raw Output'.center(w-x), curses.A_STANDOUT )
    scr.addstr( y+2, x, ''.center(w-x),           curses.A_STANDOUT )

    x = x+1
    y = y+4
    scr.addstr( y,   x,    'Repository'.ljust(14)+': ', curses.color_pair(5) )
    scr.addstr( y,   x+16, g.repo_name,                 curses.color_pair(2) )
    scr.addstr( y+1, x,    'Path'.ljust(14)+': ',       curses.color_pair(5) )
    scr.addstr( y+1, x+16, g.path,                      curses.color_pair(2) )

    lcd = commits[0].split(' ')[2]
    scr.addstr( y+2,  x,    'Last Commit'.ljust(14)+': ', curses.color_pair(5) )
    scr.addstr( y+2,  x+16, lcd,                          curses.color_pair(2) )

    y0 = y+5
    y  = y0
    scr.addstr( y,  x, 'Short History', curses.color_pair(5) )

    y, ml = render_text( scr, g.raw_hist, y+2, x, h, w )
    scr.hline( y0+1, x, curses.ACS_HLINE, w-x-1, curses.color_pair(5) )
    scr.hline( y,    x, curses.ACS_HLINE, w-x-1, curses.color_pair(5) )

    y0 = y+2
    y  = y0
    scr.addstr( y,   x, 'Status', curses.color_pair(5) )
    scr.hline ( y+1, x, curses.ACS_HLINE, w-x-1, curses.color_pair(5) )
    y, ml = render_text( scr, g.raw_status, y+2, x, h, w )

    y0 = y+2
    y  = y0
    scr.addstr( y,   x, 'Remotes', curses.color_pair(5) )
    scr.hline ( y+1, x, curses.ACS_HLINE, w-x-1, curses.color_pair(5) )
    y, ml = render_text( scr, g.raw_remotes, y+2, x, h, w )

def draw_repo_man_screen( scr ):
    scr.erase()
    y = 0
    x = 0
    h,w = scr.getmaxyx()
    scr.addstr( y, x, 'Repositories', curses.color_pair(5) )
    scr.hline( y+1, x, curses.ACS_HLINE, w-2*x, curses.color_pair(5) )

    rpsz = LGD[1][1]

    n_legs = len( LGD )

    leg = LGD[0]
    scr.addstr( y,   x,     ''.center(leg[1]), curses.A_STANDOUT )
    scr.addstr( y+1, x,   'ID'.center(leg[1]), curses.A_STANDOUT )
    scr.addstr( y+2, x,     ''.center(leg[1]), curses.A_STANDOUT )
    x = x+leg[1]+1
    scr.vline(  y,     x-1, curses.ACS_VLINE, 3 , curses.A_STANDOUT )
    scr.vline(  y+3,   x-1, curses.ACS_VLINE, NR                    )

    leg = LGD[1]
    scr.addstr( y,   x,     ''.center(leg[1]), curses.A_STANDOUT )
    scr.addstr( y+1, x,  leg[0].rjust(leg[1]), curses.A_STANDOUT )
    scr.addstr( y+2, x,     ''.center(leg[1]), curses.A_STANDOUT )
    x = x+leg[1]+1
    scr.vline(  y,     x-1, curses.ACS_VLINE, 3 , curses.A_STANDOUT )
    scr.vline(  y+3,   x-1, curses.ACS_VLINE, NR                    )

    scr.addstr( y,   x,     ''.center(w-x), curses.A_STANDOUT )
    scr.addstr( y+1, x, ' PATH'.ljust(w-x), curses.A_STANDOUT )
    scr.addstr( y+2, x,     ''.center(w-x), curses.A_STANDOUT )

    y = y + 3
    cnt = 0
    for g in GRepos:
        x = 0
        if g.repo_name == "":
            scr.hline( y+cnt, x, curses.ACS_HLINE, w-2*x, curses.color_pair(5) )
        else:
            leg = LGD[0]
            scr.addstr( y+cnt, x, (str(cnt)+' ').rjust(leg[1]) )
            x = x + leg[1]+1
            scr.addstr( y+cnt, x,  (g.repo_name+' ').rjust( rpsz ), curses.color_pair(5) )
            scr.addstr( y+cnt, x+rpsz+2, g.path )
        cnt = cnt+1



def show_message( scr, msg ):
    global display_mode
    scr.erase()
    if display_mode == 'single':
        scr.addstr( ML.h()/2, max(0,ML.w()/2-len(msg)/2), msg, curses.color_pair(2) )
        ML.refresh( scr )
    elif display_mode == 'split':
        scr.addstr( S0.h()/2, max(0,S0.w()/2-len(msg)/2), msg, curses.color_pair(2) )
        S0.refresh( scr )


def draw_legend( scr ):
    y = 1
    x = 2
    h,w = scr.getmaxyx()
    scr.addstr( y, x, 'Keybindings', curses.color_pair(5) )
    scr.hline ( y+1, x, curses.ACS_HLINE, w-2*x, curses.color_pair(5) )
    scr.addstr( y+2, x+5, 'm'.ljust(5)+': return to main screen' )
    scr.addstr( y+3, x+5, 'd'.ljust(5)+': detailed output for repo toggle (possible only in single view)' )
    scr.addstr( y+4, x+5, 'u'.ljust(5)+': update git reports' )
    scr.addstr( y+5, x+5, 'r'.ljust(5)+': repository management view' )
    scr.addstr( y+6, x+5, 'l'.ljust(5)+': display legend - toggles' )

    y = y + 8
    scr.addstr( y, x, 'Legend', curses.color_pair(5) )
    scr.hline ( y+1, x, curses.ACS_HLINE, w-2*x, curses.color_pair(5) )

    y = y+1

    cnt = 0
    for remote in remotes:
        rsymbol = remote_symbols[cnt]
        ys =     cnt/3  + 1
        xs = 15*(cnt%3) + 5
        scr.addstr( y+ys, x+xs, (rsymbol+': '+remote).ljust(15) )
        cnt += 1

    ys = len(remotes)/3 + 3
    scr.addstr( y+ys, x+5, 'S: Staged'.ljust(15) + 'C: Changed'.ljust(15) + 'U: Untracked'.ljust(15) )
    scr.border(0)


def draw_footer( scr, st ):
    h,w = scr.getmaxyx()
    scr.hline ( h-3, 1, curses.ACS_HLINE, w-2, curses.color_pair(5) )
    scr.addstr( h-2, 1, ''.center(w),          curses.color_pair(5) )
    scr.addstr( h-2, 1, st,                    curses.color_pair(5) )

def draw_selection( scr ):
    scr.move( selected_rep_id+3, 0 )
    curr_y, curr_x = scr.getyx()
    scr.chgat( curr_y, curr_x+LGD[0][1]+2, LGD[1][1]-1, curses.color_pair(2) | curses.A_BOLD )
    scr.move( 3+selected_rep_id, curr_x + LGD[0][1] + LGD[1][1] +1 )

def draw_main( scr ):
    scr.erase()
    h,w = scr.getmaxyx()

    y = 0
    x = 0

    # draw the legend
    n_legs = len( LGD )
    li = 1
    for leg in LGD:
        scr.addstr( y,   x,     ''.center(leg[1]), curses.A_STANDOUT )
        if leg[2] == 'Left':
            scr.addstr( y+1, x, leg[0].ljust(leg[1]), curses.A_STANDOUT )
        elif leg[2] == 'Center':
            scr.addstr( y+1, x, leg[0].center(leg[1]), curses.A_STANDOUT )
        elif leg[2] == 'Right':
            scr.addstr( y+1, x, leg[0].rjust(leg[1]), curses.A_STANDOUT )
        else:
            assert( 0 > 1)

        scr.addstr( y+2, x,     ''.center(leg[1]), curses.A_STANDOUT )
        x = x+leg[1]+1
        if li != n_legs:
            scr.vline(  y,     x-1, curses.ACS_VLINE, 3 , curses.A_STANDOUT    )
            scr.vline(  y+3,   x-1, curses.ACS_VLINE, NR )
        li = li+1

    # display repo reports
    y = y + 3

    cnt = 0
    for g in GRepos:
        li = 0
        x = 0
        if g.repo_name == "":
            scr.hline( y+cnt, x, curses.ACS_HLINE, w-2 )
        else:
            for leg in LGD:
                if li == 0:
                    scr.addstr( y+cnt, x, (str(cnt)+' ').rjust(leg[1]) )
                elif li == 1:
                    scr.addstr( y+cnt, x, (g.repo_name+' ').rjust(leg[1]) )
                elif li == 2:
                    scr.addstr( y+cnt, x, repo_remote_state(g).center(leg[1]) )
                elif li == 3:
                    scr.addstr( y+cnt, x, num_list_elem(g.sfiles).center(leg[1]) )
                elif li == 4:
                    scr.addstr( y+cnt, x, num_list_elem(g.cfiles).center(leg[1]) )
                elif li == 5:
                    scr.addstr( y+cnt, x, num_list_elem(g.ufiles).center(leg[1]) )
                elif li == 6:
                    scr.addstr( y+cnt, x, g.branch.center(leg[1]) )
                elif li == 7:
                    scr.addstr( y+cnt, x, var_state(g.commit).center(leg[1]) )
                x = x + leg[1]+1
                li = li+1
        cnt = cnt+1

def cache_git_reports():
    global GRepos
    for (cnt, g) in enumerate( GRepos ):
        if g.repo_name != "":
            GRepos[cnt].clear()
            GRepos[cnt].parse_status()
            GRepos[cnt].parse_remote()
            GRepos[cnt].parse_last_commit_history()

def update_layouts():
    global ML, S0, S1, L0, F0, display_mode
    global main_pad, supp_pad, msg_pad

    h,w = stdscr.getmaxyx()
    if w < 140:
        display_mode = 'single'
    else:
        display_mode = 'split'

    assert w>mw, 'Require a window bigger than width %r - Got only %r' % (mw, w)


    if display_mode == 'single':
        S0.update_screen_coords( 0, h-1, 0, mw     )
        S1.update_screen_coords( 0, h-1, mw, w-1 )

        if active_screen == 0:
            main_pad = curses.newpad( pad_h, mw )
            sw = (w-mw)/2
            sh = (h-(NR+3))/2
            ML.update_screen_coords( max(0,sh), min(h-1,sh+NR+3), max(0,sw), min(w-1,sw+mw) )
        elif active_screen == 1:
            main_pad = curses.newpad( pad_h, w  )
            ML.update_screen_coords( 0, h-1, 0, w-1 )
        elif active_screen == 3:
            main_pad = curses.newpad( pad_h, w  )
            ML.update_screen_coords( 0, h-1, 0, w-1 )
    else:
        ML.update_screen_coords( 0, h-1, 0, w-1 )
        S0.update_screen_coords( 0, h-1, 0, mw     )
        S1.update_screen_coords( 0, h-1, mw, w-1 )

        if active_screen == 0 or active_screen == 1 or active_screen == 2:
            main_pad = curses.newpad( pad_h, mw   )
            supp_pad = curses.newpad( pad_h, w-mw )
        elif active_screen == 3:
            main_pad = curses.newpad( pad_h, w-1 )

    msg_pad = curses.newpad( min(h,msg_h), w )
    F0.update_screen_coords( max(0,h-msg_h), h-1, 0, w-1 )

    if h < lgh or w < lgw:
        leg_pad = curses.newpad( h, w )
    sh = (h-1-lgh)/2
    sw = (w-1-lgw)/2
    L0.update_screen_coords( max(0,sh), min(h-1,sh+lgh), max(0,sw), min(w-1,sw+lgw) )

    main_pad.keypad(True)

    ML.erase()
    S0.erase()
    S1.erase()
    F0.erase()

def draw_content():
    global main_pad, supp_pad
    global ML, S0, S1

    if display_mode == 'single':
        if active_screen == 0:
            draw_main( main_pad )
            draw_selection( main_pad )
            ML.refresh( main_pad )
        elif active_screen == 1:
            draw_repo_details( main_pad, GRepos[selected_rep_id] )
            ML.refresh( main_pad )
        elif active_screen == 3:
            draw_repo_man_screen( main_pad )
            draw_selection( main_pad )
            ML.refresh( main_pad )
        elif active_screen == 2:
            print 'cannot draw two pads in one small screen'
            print 'should not have entered this loop'
            assert( 0 > 1 )

    elif display_mode == 'split':
        if active_screen == 2 or active_screen == 0 or active_screen == 1:
            draw_main( main_pad )
            draw_selection( main_pad )
            draw_repo_details( supp_pad, GRepos[selected_rep_id] )
            S0.refresh( main_pad  )
            S1.refresh( supp_pad )
        elif active_screen == 3:
            draw_repo_man_screen( main_pad )
            draw_selection( main_pad )
            ML.refresh( main_pad )

def config_file_add_new_repo( repo_name, repo_path ):
    f = open( CONFIG_FILE, 'a' )
    if repo_path == None and repo_name == '----':
        f.write( 'separator\n' )
    else:
        f.write( 'repo['+repo_name+']['+repo_path+']\n' )
    f.close()

def reload_repos():
    global GRepos, remotes, remote_symbols, NR
    GRepos, remotes, remote_symbols = load_config_file()
    cache_git_reports()

def load_config_file():
    global NR
    if is_valid_file(CONFIG_FILE) is False:
        print 'could not find ['+CONFIG_FILE+'] - generating dummy prototype '
        print 'there is an example .gmconfig file named gmconfig-example in the git_manager directory'
        f = open( CONFIG_FILE, 'w' )
        f.write('repo['+'repo_name'+'][repo_full_path]' '\n')
        f.write('remote['+'HEAD'+'][H]' '\n')
        f.write('remote['+'local'+'][L]' '\n')
        f.close()
        sys.exit(1)
        return None

    f = open( CONFIG_FILE, 'r+' )

    G = []
    remotes = []
    remote_symbols = []

    for r in f:
        r = r.strip()
        if r == "":
            continue
        if r[0] == '#':
            print 'Skipping Comment: ['+r+']'
            continue
        elif r == 'separator':
            repo = GitReport()
            repo.repo_name = ""
            repo.path      = ""
            G.append(repo)
        else :
            regps = re.match( r'(.*)\[(.*)\]\[(.*)\]', r, re.M)
            if regps:
                if regps.group(1) == 'repo':
                    if is_valid_dir(regps.group(3)) is False:
                        print 'Not a valid repo: ['+regps.group(2)+']['+regps.group(3)+'] - Skipping '
                        continue
                    repo = GitReport()
                    repo.repo_name = regps.group(2)
                    repo.path      = regps.group(3)
                    G.append( repo )
                if regps.group(1) == 'remote':
                    remotes.append( regps.group(2) )
                    remote_symbols.append( regps.group(3) )
                if regps.group(1) == 'repo_dir':
                    folder = regps.group(2)
                    rnames = get_folders( folder )
                    for x in rnames:
                        repo = GitReport()
                        repo.repo_name = x
                        repo.path      = folder + '/' + x
                        G.append( repo )
                if regps.group(1) == 'repo_d':
                    folder = get_home()+'/'+regps.group(3)
                    repo = GitReport()
                    repo.repo_name = regps.group(2)
                    repo.path      = folder + '/' + regps.group(2)
                    G.append( repo )

    NR  = len( G )
    f.close()
    return G, remotes, remote_symbols


#
# initialize main window legend
#
NR = 0
GRepos, remotes, remote_symbols = load_config_file()

cache_git_reports()


remote_header = ''
for rsym in remote_symbols:
    remote_header += rsym
LGD = ( ('ID '           ,  4, 'Right'),
        ('Repositories ' , 25, 'Right'),
        (remote_header   , 10, 'Center'),
        ('S '            ,  3, 'Right'),
        ('C '            ,  3, 'Right'),
        ('U '            ,  3, 'Right'),
        ('Branch'        , 10, 'Center'),
        ('Dirty'        ,  10, 'Center') )

mw = len( LGD )-1
for (i, leg) in enumerate( LGD ):
    mw += leg[1]


if NR == 0:
    print ' No repo configured'
    print
    print ' Create the '+CONFIG_FILE+' file and add entries like:'
    print
    print '     repo[repo_name][repo_full_path]'
    print '     remote[remote_name][remote_symbol]'
    print
    print ' For example:'
    print
    print '     repo[kortex][/home/tola/src/cpp/lib/kortex]'
    print '     repo[KX-OCV][/home/tola/src/cpp/lib/kortex-ext-opencv]'
    print '     remote[HEAD][H]'
    print '     remote[borg][B]'
    print '     remote[local][L]'
    print
    print
    sys.exit(1)

msg_h = 2
msg_w = 80

lgh = 20
lgw = 80

selected_rep_id = 0


try:

    stdscr = curses.initscr()
    stdscr.erase()
    curses.cbreak()
    curses.noecho()

    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    h,w = stdscr.getmaxyx()

    pad_h = 200

    main_pad = curses.newpad( pad_h, mw )
    main_pad.keypad(True)
    main_pad.border(0)
    main_pad.addstr(0, 0, 'main' )

    supp_pad = curses.newpad( pad_h, 100 )
    supp_pad.keypad(True)
    supp_pad.border(0)
    supp_pad.addstr(0, 0, 'support' )

    leg_pad = curses.newpad(lgh,lgw)
    leg_pad.border(0)

    msg_pad = curses.newpad( msg_h, w )

    ML = Layout()
    S0 = Layout()
    S1 = Layout()
    L0 = Layout()
    F0 = Layout()

    active_screen = 0
    display_mode = 'single'

    update_layouts()
    stdscr.refresh()

    update_main = False

    dl = 0
    k = 0
    while k!= ord('q'):

        update_support = False
        update_main    = False

        if k == curses.KEY_RESIZE:
            update_layouts()
            stdscr.refresh() # makes sure during get_input screen is not empty

        elif k == curses.KEY_DOWN:
            selected_rep_id = selected_rep_id + 1
            if selected_rep_id >= NR-1:
                selected_rep_id=NR-1
            if GRepos[selected_rep_id].repo_name == "":
                selected_rep_id=selected_rep_id+1
            if selected_rep_id >= NR-1:
                selected_rep_id=NR-1

        elif k == curses.KEY_UP:
            selected_rep_id = selected_rep_id - 1
            if selected_rep_id < 0:
                selected_rep_id=0
            if GRepos[selected_rep_id].repo_name == "":
                selected_rep_id=selected_rep_id-1
            if selected_rep_id < 0:
                selected_rep_id=0

        elif k == ord('d'):
            if display_mode == 'single':
                if active_screen == 1:
                    active_screen = 0
                elif active_screen == 0:
                    active_screen = 1
            if active_screen == 3:
                active_screen = 1
            update_layouts()

        elif k == ord('r'):
            active_screen = 3
            update_layouts()

        elif k == ord('m'):
            active_screen = 0
            update_layouts()

        elif k == ord('u'):
            show_message( main_pad, 'Updating Repo Info')
            cache_git_reports()

        elif k == ord('l') or k == ord('h'):
            dl = (dl+1)%2
            if dl==0:
                L0.erase()

        elif k == ord('c'):
            get_input( stdscr )

        elif active_screen == 3 and k == ord('a'):
            add_new_repo( stdscr )

        draw_content()

        if dl == 1:
            draw_legend( leg_pad )
            L0.refresh( leg_pad )

        h,w = stdscr.getmaxyx()
        msg_pad.hline( 0, 0, curses.ACS_HLINE, w, curses.color_pair(5) )
        msg_pad.addstr( 0, 0, str(NR) )

        msg_pad.addstr( 1, w-4, str(w) )
        F0.refresh( msg_pad )
        # curses.napms(100)

        k = main_pad.getch()
        msg_pad.erase()
        # F0.erase()

finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
