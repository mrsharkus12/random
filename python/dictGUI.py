import curses
import json

isProgramActive = True

SampledictData = {"john": {"occupation": "director", "wage": 1500}}
DefaultFileName = "Default.json"

# VSCode sucks balls >:(
Debug_VSCodeInput = True
TerminalKeys = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_RIGHT, curses.KEY_LEFT] 
VSCodeKeys = [curses.KEY_A2, curses.KEY_C2, curses.KEY_B3, curses.KEY_B1]

if Debug_VSCodeInput:
    inputKeys = VSCodeKeys
else:
    inputKeys = TerminalKeys

# def file creation
try:
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dictData = string
        # print(f"Successfully read {DefaultFileName}")
except FileNotFoundError:
    # create a sample file
    with open(DefaultFileName, "w") as file:
        string = json.dumps(SampledictData)
        file.write(string)
    # print(f"Successfully saved to {DefaultFileName}")
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dictData = string
        # print(f"Successfully read {DefaultFileName}")

# submenus
def editMenu(stdscr):
    global dictData
    try:
        tempdictData = dictData
    except TypeError:
        stdscr.addstr(15, 0, "Fatal error!!!", curses.color_pair(2))

    key = ""
    sel = 0
    options = ["Add/Edit Item", "Back"]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Edit Menu")
        for index, option in enumerate(options):
            if index == sel:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(1))
            else:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(0))

        key = stdscr.getch()

        if key == inputKeys[0]:
            sel = (sel - 1) % len(options)
        elif key == inputKeys[1]:
            sel = (sel + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10):
            if sel == 0:  # Add/Edit Item
                stdscr.clear()
                stdscr.addstr(0, 0, "Add/Edit Item")
                
                curses.echo()
                stdscr.addstr(2, 0, "Name: ")
                name = stdscr.getstr(2, 6).decode('utf-8')
                stdscr.addstr(3, 0, "Parameter: ")
                param = stdscr.getstr(3, 11).decode('utf-8')
                stdscr.addstr(4, 0, "Value: ")
                val = stdscr.getstr(4, 6).decode('utf-8')
                curses.noecho()

                editType = ""
                if name not in tempdictData:
                    tempdictData[name] = {}
                    editType = "Added"
                else:
                    editType = "Edited"
                tempdictData[name][param] = val

                stdscr.addstr(6, 0, f"{editType} {name}'s {param} to {val}")
                stdscr.refresh()
                stdscr.getch()
            elif sel == 1:
                break
def viewMenu(stdscr):
    global dictData
    key = ""

    try:
        tempdictData = dictData
    except TypeError:
        stdscr.addstr(15, 0, "Fatal error!!!", curses.color_pair(2))

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "View")

        try:
            if not tempdictData:
                stdscr.addstr(1, 0, "No items to display.")
            else:
                row = 2
                for name, params in tempdictData.items():
                    stdscr.addstr(row, 0, f"{name}:")
                    row += 1
                    for param, value in params.items():
                        stdscr.addstr(row, 2, f"  {param} = {value}")
                        row += 1
        except AttributeError:
            stdscr.addstr(3, 0, "Error reading loaded file, please load a proper file or load a default!", curses.color_pair(2))
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10):
                break
        stdscr.addstr(row + 1, 0, "Press Enter to go back.", curses.color_pair(1))
        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10):
            break
def deleteMenu(stdscr):
    global dictData
    key = ""

    try:
        tempdictData = dictData
    except TypeError:
        stdscr.addstr(15, 0, "Fatal error!!!", curses.color_pair(2))

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Delete")

        curses.echo()
        stdscr.addstr(2, 0, "Name: ")
        name = stdscr.getstr(2, 6).decode('utf-8')

        try:
            del tempdictData[name]
            stdscr.addstr(4, 0, f"Removed {name} from current dictDataionary")
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10):
                break
        except KeyError:
            stdscr.addstr(4, 0, f"Item does not exist in current list.", curses.color_pair(2))
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10):
                break
def saveMenu(stdscr):
    key = ""
    global dictData

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Save into File")

        curses.echo()
        stdscr.addstr(2, 0, "File Name: ")
        fileName = stdscr.getstr(2, 11).decode('utf-8')

        if not fileName.endswith('.json'):
            fileName = fileName + ".json"

        try:
            with open(fileName, "w") as file:
                string = json.dumps(dictData)
                file.write(string)
            stdscr.addstr(4, 0, f"Successfully saved to {fileName}")
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()
            if key in (curses.KEY_ENTER, 10):
                break
        except OSError:
            stdscr.addstr(4, 0, "Invalid character used.", curses.color_pair(2))
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10):
                break
def loadMenu(stdscr):
    key = ""
    global dictData

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Load from File")

        curses.echo()
        stdscr.addstr(2, 0, "File Name: ")
        fileName = stdscr.getstr(2, 11).decode('utf-8')
        if fileName == "":
            break

        if not fileName.endswith('.json'):
            fileName = fileName + ".json"
        try:
            with open(fileName, "r") as file:
                dictData = json.load(file)
            stdscr.addstr(4, 0, f"Successfully read {fileName}")
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()
            if key in (curses.KEY_ENTER, 10):
                break
        except FileNotFoundError: # File not found handler
            stdscr.addstr(4, 0, "File not found.", curses.color_pair(2))
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10):
                break
        except json.JSONDecodeError: # Decode error handler
            stdscr.addstr(4, 0, "File not found.", curses.color_pair(2))
            stdscr.refresh()
            stdscr.addstr(5, 0, "Press Enter to go back.", curses.color_pair(1))
            key = stdscr.getch()

            if key in (curses.KEY_ENTER, 10):
                break
def quitMenu(stdscr):
    key = ""
    sel = 0
    options = ["No", "Yes"]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Are you sure you want to quit?")
        for index, option in enumerate(options):
            if index == sel:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(2))
            else:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(0))

        key = stdscr.getch()

        if key == inputKeys[0]:
            sel = (sel-1)%len(options)
        elif key == inputKeys[1]:
            sel = (sel+1)%len(options)
        elif key in (curses.KEY_ENTER, 10):
            if sel == 0: # Edit
                return False
            elif sel == 1: # Edit
                return True
# main menu
def mainGUI(stdscr):
    global isProgramActive

    key = ""
    sel = 0
    options = ["Edit", "View", "Delete", "Load", "Save", "Exit"]

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Highlighted Priority
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED) # Highlighted Error

    stdscr.clear()
    while isProgramActive:
        stdscr.clear()

        stdscr.addstr(0, 0, "Select Option")
        for index, option in enumerate(options):
            if index == sel:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(1))
            else:
                stdscr.addstr(index + 1, 0, option, curses.color_pair(0))

        key = stdscr.getch()
        
        if key == inputKeys[0]:
            sel = (sel-1)%len(options)
        elif key == inputKeys[1]:
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
                if quitMenu(stdscr):
                    isProgramActive = False

        stdscr.refresh()
# execute
curses.wrapper(mainGUI)