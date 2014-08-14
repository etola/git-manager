#! /usr/bin/env python

import sys, os, curses, re, math

# from utility              import *
# from gm_resources         import *
from gm_core              import *

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
    remotes, remote_symbols = get_remote_names()
    cnt = 0
    for remote in remotes:
        rsymbol = remote_symbols[cnt]
        msg += rep_state( remote, g.lcsyncrem, rsymbol )
        cnt += 1
    return msg

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

    y = DY
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

    # scr.addstr( h-1, w-1, '' )

def draw_legend( scr ):
    y = 1
    x = 2
    h,w = scr.getmaxyx()
    scr.addstr( y, x, 'Keybindings', curses.color_pair(5) )
    scr.hline ( y+1, x, curses.ACS_HLINE, w-2*x, curses.color_pair(5) )
    scr.addstr( y+2, x+5, 'd'.ljust(5)+': detailed output for repo toggle' )
    scr.addstr( y+3, x+5, 'u'.ljust(5)+': update git reports' )

    y = y + 5
    scr.addstr( y, x, 'Legend', curses.color_pair(5) )
    scr.hline ( y+1, x, curses.ACS_HLINE, w-2*x, curses.color_pair(5) )

    y = y+1


    remotes, remote_symbols = get_remote_names()

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

def draw_main( scr ):

    scr.erase()

    global Y0
    global X0
    Y0 = DY
    X0 = DX

    h,w = scr.getmaxyx()

    # draw the legend
    n_legs = len( LGD )
    li = 1
    for leg in LGD:
        scr.addstr( Y0,   X0,     ''.center(leg[1]), curses.A_STANDOUT )
        if leg[2] == 'Left':
            scr.addstr( Y0+1, X0, leg[0].ljust(leg[1]), curses.A_STANDOUT )
        elif leg[2] == 'Center':
            scr.addstr( Y0+1, X0, leg[0].center(leg[1]), curses.A_STANDOUT )
        elif leg[2] == 'Right':
            scr.addstr( Y0+1, X0, leg[0].rjust(leg[1]), curses.A_STANDOUT )
        else:
            assert( 0 > 1)

        scr.addstr( Y0+2, X0,     ''.center(leg[1]), curses.A_STANDOUT )
        X0 = X0+leg[1]+1
        if li != n_legs:
            scr.vline(  Y0,     X0-1, curses.ACS_VLINE, 3 , curses.A_STANDOUT    )
            scr.vline(  Y0+3,   X0-1, curses.ACS_VLINE, NR )
        li = li+1

    LGSZ = X0-DX-1

    # display repo reports
    Y0 = DY + 3
    X0 = DX
    cnt = 0
    for repo in rep_names:
        g = G[cnt]
        li = 0
        x = X0
        if g.repo_name == "":
            scr.hline( Y0+cnt, x, curses.ACS_HLINE, LGSZ )
        else:
            for leg in LGD:
                if li == 0:
                    scr.addstr( Y0+cnt, x, (str(cnt)+' ').rjust(leg[1]) )
                elif li == 1:
                    scr.addstr( Y0+cnt, x, (repo+' ').rjust(leg[1]) )
                elif li == 2:
                    scr.addstr( Y0+cnt, x, repo_remote_state(g).center(leg[1]) )
                elif li == 3:
                    scr.addstr( Y0+cnt, x, num_list_elem(g.sfiles).center(leg[1]) )
                elif li == 4:
                    scr.addstr( Y0+cnt, x, num_list_elem(g.cfiles).center(leg[1]) )
                elif li == 5:
                    scr.addstr( Y0+cnt, x, num_list_elem(g.ufiles).center(leg[1]) )
                elif li == 6:
                    scr.addstr( Y0+cnt, x, g.branch.center(leg[1]) )
                elif li == 7:
                    scr.addstr( Y0+cnt, x, var_state(g.commit).center(leg[1]) )
                x = x + leg[1]+1
                li = li+1
        cnt = cnt+1

    scr.move( DY+3+SELR, DX )
    curr_y, curr_x = scr.getyx()
    scr.chgat( curr_y, curr_x+LGD[0][1]+2, LGD[1][1]-1, curses.color_pair(2) | curses.A_BOLD )
    scr.move( DY+3+SELR, curr_x + LGD[0][1] + LGD[1][1] +1 )
    # scr.border(0)

    # scr.addstr( h-1, w-1, '' )

def cache_git_reports():
    global G
    c = 0
    for repo in rep_names:
        G[c] = generate_git_report( repo )
        c = c+1



rep_names = get_repositories()

NR  = len( rep_names )
G = [None] * NR

mh = max(NR+10,20)    # main pad height
mw = 75               # main pad width
sh = 200              # support pad height
sw_default = 100      # support pad default width
sw = sw_default       # support pad active width
lh = 20               # legend pad height
lw = 80               # legend pad width
dual_mode = False     # initialially we start with only the main pad

#
# initialize main window legend
#
remotes, remote_symbols = get_remote_names()
remote_header = ''
for rsym in remote_symbols:
    remote_header += rsym
LGD = ( ('ID '           , 4 , 'Right'),
        ('Repositories ' , 25, 'Right'),
        (remote_header   , 10, 'Center'),
        ('S '            , 3 , 'Right'),
        ('C '            , 3 , 'Right'),
        ('U '            , 3 , 'Right'),
        ('Branch'        , 8 , 'Center'),
        ('Dirty'        , 10, 'Center') )

# start curses
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()

# color setup
curses.start_color()
curses.use_default_colors()
for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, i, -1)

def update_pad_dimensions():
    global LY, LX, fw, fh, dual_mode, sw

    fh,fw = stdscr.getmaxyx()
    LY = 0
    LX = 0
    if fw < mw+sw_default:
        LX = (fw-mw)/2
        LY = (fh-mh)/2
        dual_mode = False
        sw = fw
    else:
        LX = 0
        LY = 0
        sw = fw - mw -1
        dual_mode = True


DY  =  0
DX  =  1
SELR = 0
ACTIVE_SCREEN = 0

try:

    update_pad_dimensions()

    win_main   = curses.newpad(mh,mw)
    win_supp   = curses.newpad(sh,sw)
    win_legend = curses.newpad(lh,lw)

    dl = 0
    win_main.keypad(True)

    cache_git_reports()
    k=0
    while k != ord('q'):

        win_main.erase()

        if k == curses.KEY_DOWN:
            SELR = SELR + 1
            if SELR >= NR-1:
                SELR=NR-1
            if G[SELR].repo_name == "":
                SELR=SELR+1
            if SELR >= NR-1:
                SELR=NR-1

        elif k == curses.KEY_UP:
            SELR = SELR - 1
            if SELR < 0:
                SELR=0
            if G[SELR].repo_name == "":
                SELR=SELR-1
            if SELR < 0:
                SELR=0

        elif k == ord('u'):
            win_main.erase()
            st = 'Updating Repo Info'
            win_main.addstr( mh/2, mw/2-len(st)/2, st, curses.color_pair(2) )
            win_main.refresh(0,0, LY, LX, min(fh-1,LY+mh), min(fw-1,LX+mw) )
            cache_git_reports()

        elif k == ord('h'):
            if dl == 1:
                win_legend.erase()
                win_legend.refresh(0, 0, max(0,fh/2-lh/2), max(0,fw/2-lw/2), min(fh-1,fh/2+lh/2), min(fw-1,fw/2+lw/2) )
            dl = (dl+1)%2

        elif k == ord('d'):
            if dual_mode is False:
                ACTIVE_SCREEN = (ACTIVE_SCREEN+1)%2
                stdscr.erase()
                stdscr.refresh()
            else:
                ACTIVE_SCREEN = 0

            update_pad_dimensions()
            win_supp = curses.newpad(sh,sw)


        elif k == curses.KEY_RESIZE:
            stdscr.erase()
            stdscr.refresh()
            update_pad_dimensions()
            win_supp = curses.newpad(sh,sw)

        if ACTIVE_SCREEN == 0:
            draw_main( win_main )
            if dual_mode is False:
                draw_footer( win_main, 'Press d for detailed view: ['+G[SELR].repo_name +']' )
            win_main.refresh(0, 0, LY, LX, min(fh-1,LY+mh), min(fw-1,LX+mw) )
            if fw > mw + sw:
                draw_repo_details( win_supp, G[SELR] )
                win_supp.refresh( 0, 0, LY, LX+mw, min(fh-1,LY+sh-1), min(fw-1,LX+mw+sw-1)  )
            else:
                win_supp.erase()
                win_supp.refresh( 0, 0, LY, LX+mw, min(fh-1,LY+sh-1), min(fw-1,LX+mw+sw-1)  )
        elif ACTIVE_SCREEN == 1:
            draw_repo_details( win_supp, G[SELR] )
            win_supp.refresh( 0, 0, 0, 0, min(fh-1,sh-1), min(fw-1,sw-1)  )

        if dl == 1:
            draw_legend( win_legend )
            win_legend.refresh(0, 0, max(0,fh/2-lh/2), max(0,fw/2-lw/2), min(fh-1,fh/2+lh/2), min(fw-1,fw/2+lw/2) )

        k = win_main.getch()

    pass

finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
