try:
    ## frame controllers
    from tkinter import *
    from tkinter import ttk
    from tkinter import font
    from tkinter import filedialog
    from tkinter import messagebox

    ## file extension controllers
    import os
    import json
    import csv

    ## SQL controllers
    import psycopg2
except ModuleNotFoundError:
    print("Critical modules not found.")
    quit()
except Exception as e:
    print("Error", f"An error occurred: {str(e)}")

## windows params
MainWindow_Title = "Title"
MainWindow_ResWidth = "640"
MainWindow_ResHeight = "350"

AddWindow_Title = "Add an entry..."
AddWindow_ResWidth = "250"
AddWindow_ResHeight = "0"

SettingsWindow_Title = "Settings"
SettingsWindow_ResWidth = "240"
SettingsWindow_ResHeight = "240"

## supported file types
supportedToLoadTypes = [('JavaScript Object Notation', '*.json'), ('Comma Separated Values', '*.csv'), ('All files', '*')]
supportedToSaveTypes = [('JavaScript Object Notation', '*.json'), ('Comma Separated Values', '*.csv'), ('All files', '*')]

## SQL settings
IsSQLEnabled = False
DB_HOST = 'localhost'
DB_NAME = 'TestDB'
DB_USER = 'postgres'
DB_PASSWORD = '123'

## DB connection
def connect_db():
    if IsSQLEnabled:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

## default file
TestList = {
    "John": {"Occupation": "Director", "Salary": 1500},
    "Jane": {"Occupation": "Developer", "Salary": 1200},
    "Doe": {"Occupation": "Designer", "Salary": 1300},
}
DefaultFileName = "Default.json"

## default file creation
def defFileCreation(fileName):
    global dictData

    try:
        with open(fileName, "r", encoding='utf-8') as file:
            string = json.load(file)
            dictData = string
    except FileNotFoundError:
        with open(fileName, "w") as file:
            string = json.dumps(TestList, ensure_ascii=False, indent=4)
            file.write(string)
        with open(fileName, "r", encoding='utf-8') as file:
            string = json.load(file)
            dictData = string

## Converters
def CSVformatConvert(nestedDict):
    flat_list = []
    for key, value in nestedDict.items():
        flat_dict = {'name': key}
        flat_dict.update(value)
        flat_list.append(flat_dict)
    return flat_list

def JSONformatConvert(file_path):
    nested_dict = {}
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            nested_dict[name] = {k: row[k] for k in row if k != 'name'}
    return nested_dict

#### Main
## UI
class UI(Frame):
    global dictData

    def __init__(self, master):
        defFileCreation(DefaultFileName)    # create default file

        Frame.__init__(self, master)
        self.master = master
        self.DeletionToggle = BooleanVar()
        self.base_Window()

        self.editing = False
        self.current_item = None 
        self.current_column = None
        self.entry = None


    def base_Window(self):
        global dictData

        self.master.title(MainWindow_Title)
        self.master.geometry(MainWindow_ResWidth + "x" + MainWindow_ResHeight)
        self.master.resizable(False, False)

        mainMenu = Menu(self.master, tearoff=0)
        fileMenu = Menu(mainMenu, tearoff=0)
        editMenu = Menu(mainMenu, tearoff=0)
 
        fileMenu.add_command(label="Save", command=self.saveFile_Ask)
        fileMenu.add_command(label="Load", command=self.loadFile_Ask)
        fileMenu.add_separator()
        fileMenu.add_command(label="Settings", command=self.settings_Window)
        fileMenu.add_command(label="Exit", command=root.quit)

        editMenu.add_command(label="Add an Entry", command=self.addEntry_Window)
        editMenu.add_command(label="Add/Edit Columns")
        editMenu.add_separator()
        editMenu.add_checkbutton(label="Delete", onvalue=1, offvalue=0, variable=self.DeletionToggle)

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

            
        def deleteEntry(self):
            if self.DeletionToggle.get():  # Check if deletion is toggled on
                selected_item = self.tree.selection()  # Get the selected item
                if selected_item:  # If there is a selected item
                    item_values = self.tree.item(selected_item, 'values')  # Get the values of the selected item
                    name_to_delete = item_values[0]  # Assuming the first column is the name

                    # Remove from dictData
                    if name_to_delete in dictData:
                        del dictData[name_to_delete]

                    # Remove from the Treeview
                    self.tree.delete(selected_item)

        self.tree.bind("<Double-1>", self.mouseDoubleClick)

    # Double click event
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

    def addEntry_Window(self):
        win = Tk()
        win.title(AddWindow_Title)
        win.geometry(AddWindow_ResWidth + "x" + AddWindow_ResHeight)
        win.attributes("-toolwindow", True)
        win.resizable(False, False)

        frame = ttk.Frame(win)
        frame.pack(padx=8, pady=8)

        current_height = int(AddWindow_ResHeight)

        def add_entry():
            nonlocal current_height
            entry = ttk.Entry(frame)
            entry.pack(anchor=NW, padx=8, pady=5)

            button = ttk.Button(frame, text="+", command=add_entry)
            button.pack(anchor=NE, padx=8, pady=0)

            current_height += 100
            win.geometry(AddWindow_ResWidth + "x" + str(current_height))

        add_entry()

        submit_button = ttk.Button(win, text="Submit", command=lambda: self.handle_entries(frame))
        submit_button.pack(anchor=SE, padx=8, pady=8)

    def handle_entries(self, frame):
        entries = frame.winfo_children()
        data = []
        for widget in entries:
            if isinstance(widget, ttk.Entry):
                data.append(widget.get())
        
        print(data)

        frame.master.destroy()

    def settings_Window(self):
        win = Tk()
        win.title(SettingsWindow_Title)
        win.geometry(SettingsWindow_ResWidth + "x" + SettingsWindow_ResHeight)
        win.attributes("-toolwindow", True)
        win.resizable(False, False)

        ttk.Button(win, text="Recreate Default File", command=defFileCreation(DefaultFileName)).pack(anchor=NW, padx=8, pady=8)

    # Opens file selection dialog
    def loadFile_Ask(self):
        global dictData

        dlg = filedialog.askopenfilename(filetypes=supportedToLoadTypes, defaultextension=".json")

        if not dlg: return
        try:
            if dlg.endswith('.json'):
                with open(dlg, "r") as file:
                    dictData = json.load(file)
            elif dlg.endswith('.csv'):
                dictData = JSONformatConvert(dlg)
            else:
                messagebox.showerror("Error", "Unsupported file type.")
                return

            for item in self.tree.get_children():
                self.tree.delete(item)

            for name, details in dictData.items():
                populate = [name] + [details[key] for key in details.keys()]
                self.tree.insert("", "end", values=populate)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to decode JSON. Please check the file format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Opens file selection dialog (as save)
    def saveFile_Ask(self):
        global dictData

        dlg = filedialog.asksaveasfilename(filetypes=supportedToSaveTypes, defaultextension=".json")
        
        if not dlg: return
        if dlg.endswith('.json'):
            with open(dlg, "w") as file:
                string = json.dumps(dictData, ensure_ascii=False, indent=4)
                file.write(string)
        elif dlg.endswith('.csv'):
            converted = CSVformatConvert(dictData)
            with open(dlg, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=converted[0].keys())
                writer.writeheader()
                writer.writerows(converted)

# start the app
root = Tk()
app = UI(root)
root.mainloop()
