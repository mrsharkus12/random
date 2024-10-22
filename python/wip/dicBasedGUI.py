AppName = "mrsharksu's based app >:)"
ResolutionWidth = "640"
ResolutionHeight = "480"

## frame controllers
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

## SQL controllers
import psycopg2       # postgresql

## UI
class UI(Frame):
    # some tkinter shenanigans
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master = master
        self.base()

    # main menu
    def base(self):
        self.master.title(AppName)
        self.master.geometry(ResolutionWidth + "x" + ResolutionHeight)
        self.master.attributes("-toolwindow", True)
        self.master.resizable(True, True)

        self.master.option_add("*tearOff", False)

        mainMenu = Menu()
        fileMenu = Menu()
        editMenu = Menu()

        fileMenu.add_command(label="Save")
        fileMenu.add_command(label="Load", command=self.loadFile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=root.quit)

        editMenu.add_command(label="Add")
        editMenu.add_command(label="Edit")
        editMenu.add_command(label="Delete")

        mainMenu.add_cascade(label="File", menu=fileMenu)
        mainMenu.add_cascade(label="Editing", menu=editMenu)

        self.master.config(menu=mainMenu)
        
        colAmount = 0
        tree = ttk.Treeview(columns=list(range(colAmount)), show="headings")
        tree.grid(row=0, column=0, rowspan=2, ipadx=6, ipady=55, padx=5, pady=5)

        for l in range(colAmount):
            tree.column(l, stretch=0, width=150)

        scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

    def loadFile(self):
        supportedTypes = [('JSON', '*.json'), ('CSV', '*.csv'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = supportedTypes)
        dlg.show()

# start the app
root = Tk()
app = UI(root)
root.mainloop()