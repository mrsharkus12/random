import curses

def mainGUI(stdscr):
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
            sel = (sel - 1)%len(options)
        elif key == curses.KEY_DOWN:
            sel = (sel + 1)%len(options)
        elif key in (curses.KEY_ENTER, 10):
            if sel == 0:
                print("test!!!")
            elif sel == 1:
                print("test!!!")
            elif sel == 2:
                print("test!!!")
            elif sel == 3:
                print("test!!!")
            elif sel == 4:
                print("test!!!")
            elif sel == 5:
                break

        stdscr.refresh()

curses.wrapper(mainGUI)
