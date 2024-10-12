import curses

def main(stdscr):
    key = ""
    sel = 0
    options = ["Edit", "View", "Delete", "Load", "Save", "Exit"]

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    while True:
        stdscr.clear()

        stdscr.addstr(0, 0, "Select Option")
        for index, option in enumerate(options):
            if index == sel:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(1))
            else:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(0))

        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            sel = (sel - 1)
        elif key == curses.KEY_DOWN:
            sel = (sel + 1)
        elif key == ord('q'):
            break

        stdscr.refresh()

curses.wrapper(main)
