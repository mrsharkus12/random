import curses

def editMenu(stdscr):
    key = ""
    sel = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "submenu 1")

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10):
            break
        else:
            stdscr.refresh()
            stdscr.getch()
def viewMenu(stdscr):
    key = ""
    sel = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "submenu 2")

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10):
            break
        else:
            stdscr.refresh()
            stdscr.getch()
def deleteMenu(stdscr):
    key = ""
    sel = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "submenu 3")

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10):
            break
        else:
            stdscr.refresh()
            stdscr.getch()
def saveMenu(stdscr):
    key = ""
    sel = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "submenu 4")

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10):
            break
        else:
            stdscr.refresh()
            stdscr.getch()
def loadMenu(stdscr):
    key = ""
    sel = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "submenu 5")

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10):
            break
        else:
            stdscr.refresh()
            stdscr.getch()

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
            sel = (sel-1)%len(options)
        elif key == curses.KEY_DOWN:
            sel = (sel+1)%len(options)
        elif key in (curses.KEY_ENTER, 10):
            if sel == 0: # Edit
                editMenu(stdscr)
            elif sel == 1: # View
                viewMenu(stdscr)
            elif sel == 2: # Delete
                deleteMenu(stdscr)
            elif sel == 3: # Load
                loadMenu(stdscr)
            elif sel == 4: # Save
                saveMenu(stdscr)
            elif sel == 5: # Exit
                break

        stdscr.refresh()

curses.wrapper(mainGUI)
