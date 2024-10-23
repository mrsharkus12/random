AppName = "mrsharksu's based app >:)"
ResolutionWidth = "800"
ResolutionHeight = "600"

## frame controllers
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox

import os
import json
import csv

TestList = {
    "john": {"occupation": "director", "wage": 1500},
    "jane": {"occupation": "developer", "wage": 1200},
    "doe": {"occupation": "designer", "wage": 1300},
}
DefaultFileName = "Default.json"

# default file creation
try:
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dictData = string
except FileNotFoundError:
    with open(DefaultFileName, "w") as file:
        string = json.dumps(TestList, ensure_ascii=False, indent=4)
        file.write(string)
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dictData = string

## UI
class UI(Frame):
    global dictData

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.base()
        self.editing = False
        self.current_item = None 
        self.current_column = None
        self.entry = None

    def base(self):
        global dictData

        self.master.title(AppName)
        self.master.geometry(ResolutionWidth + "x" + ResolutionHeight)  # Example resolution
        self.master.attributes("-toolwindow", True)
        self.master.resizable(False, False)

        self.master.option_add("*tearOff", False)

        mainMenu = Menu()
        fileMenu = Menu()
        editMenu = Menu()

        fileMenu.add_command(label="Save", command=self.saveFile)
        fileMenu.add_command(label="Load", command=self.loadFile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=root.quit)

        editMenu.add_command(label="Add", command=self.testWindow)
        editMenu.add_command(label="Edit")
        editMenu.add_command(label="Delete")

        mainMenu.add_cascade(label="File", menu=fileMenu)
        mainMenu.add_cascade(label="Editing", menu=editMenu)

        self.master.config(menu=mainMenu)

        if dictData:
            colAmount = len(next(iter(dictData.values())).keys()) + 1
        else:
            colAmount = 0

        self.tree = ttk.Treeview(columns=list(range(colAmount)), show="headings")
        self.tree.grid(row=0, column=0, rowspan=2, ipadx=6, ipady=55, padx=5, pady=5)

        self.tree.heading(0, text="Name")
        for index, key in enumerate(next(iter(dictData.values())).keys(), start=1):
            self.tree.heading(index, text=key)

        for name, details in dictData.items():
            populate = [name] + [details[key] for key in details.keys()]
            self.tree.insert("", "end", values=populate)

        scrollbar = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<Double-1>", self.mouseDoubleClick)

    def mouseDoubleClick(self, event):
        if self.editing:
            return
        
        item = self.tree.selection()[0]
        self.current_item = item
        self.current_column = self.tree.identify_column(event.x)

        column_index = int(self.current_column.replace("#", "")) - 1
        current_value = self.tree.item(item, "values")[column_index]

        self.entry = Entry(self.master)
        self.entry.insert(0, current_value)
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        self.entry.focus()
        self.entry.bind("<Return>", self.startEdit)

        self.editing = True

    def startEdit(self, event):
        if not self.editing:
            return

        new_value = self.entry.get()
        column_index = int(self.current_column.replace("#", "")) - 1
        updated_values = self.finishEdit(column_index, new_value)

        self.tree.item(self.current_item, values=updated_values)
        self.entry.destroy()
        self.editing = False

    def finishEdit(self, column_index, new_value):
        current_values = list(self.tree.item(self.current_item, "values"))
        current_values[column_index] = new_value

        name = current_values[0]
        if column_index == 0:
            old_name = self.tree.item(self.current_item, "values")[0]
            if old_name in dictData:
                dictData[new_value] = dictData.pop(old_name)
        else:
            if name in dictData:
                keys = list(dictData[name].keys())
                if column_index - 1 < len(keys):
                    dictData[name][keys[column_index - 1]] = new_value

        return current_values

    def testWindow(self):
        win = Tk()
        win.title("AppName")
        win.geometry("800x600")
        win.attributes("-toolwindow", True)
        win.resizable(False, False)

    def loadFile(self):
        global dictData

        supportedTypes = [('JavaScript Object Notation', '*.json'), ('Comma Separated Values', '*.csv'), ('All files', '*')]
        dlg = filedialog.askopenfilename(filetypes=supportedTypes, defaultextension=".json")

        if not dlg: return
        try:
            with open(dlg, "r") as file:
                dictData = json.load(file)

            for item in self.tree.get_children():
                self.tree.delete(item)

            for name, details in dictData.items():
                populate = [name] + [details[key] for key in details.keys()]
                self.tree.insert("", "end", values=populate)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to decode JSON. Please check the file format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def saveFile(self):
        global dictData

        supportedTypes = [('JavaScript Object Notation', '*.json'), ('Comma Separated Values', '*.csv'), ('All files', '*')]
        dlg = filedialog.asksaveasfilename(filetypes=supportedTypes, defaultextension=".json")
        
        if not dlg: return
        with open(dlg, "w") as file:
            string = json.dumps(dictData, ensure_ascii=False, indent=4)
            file.write(string)

# start the app
root = Tk()
app = UI(root)
root.mainloop()
