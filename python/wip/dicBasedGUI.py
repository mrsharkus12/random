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
MainWindow_Title = "Main"
MainWindow_ResWidth = "640"
MainWindow_ResHeight = "350"

AddWindow_Title = "Add an entry..."
AddWindow_ResWidth = "165"
AddWindow_ResHeight = "165"

SettingsWindow_Title = "Settings"
SettingsWindow_ResWidth = "240"
SettingsWindow_ResHeight = "240"

CMDWindow_Title = "SQL Command Line"
CMDWindow_ResWidth = "500"
CMDWindow_ResHeight = "250"

## supported file types
supportedToLoadTypes = [('JavaScript Object Notation', '*.json'), ('Comma Separated Values', '*.csv'), ('All files', '*')]
supportedToSaveTypes = [('JavaScript Object Notation', '*.json'), ('Comma Separated Values', '*.csv'), ('All files', '*')]

## default file
TestList = {
    "John": {"Occupation": "Director", "Salary": 1500},
    "Jane": {"Occupation": "Developer", "Salary": 1200},
    "Doe": {"Occupation": "Designer", "Salary": 1300},
}
DefaultFileName = "Default.json"

DefaultConfig = {
    "general": {"sql_enabled": False},
    "sql": {"hostname": "localhost", "name": "TestDB", "user": "postgres", "password": "123"},
}
DefaultConfigFileName = "config.json"

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

## config file creation
def cfgFileCreation(fileName):
    try:
        with open(fileName, "r", encoding='utf-8') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        with open(fileName, "w") as file:
            string = json.dumps(DefaultConfig, ensure_ascii=False, indent=4)
            file.write(string)
        with open(fileName, "r", encoding='utf-8') as file:
            config = json.load(file)
            return config

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

## DB connection \ executing
def ConnectDB(config):
    sql_config = config.get_sql_config()
    
    return psycopg2.connect(
        host=sql_config['host'],
        database=sql_config['database'],
        user=sql_config['user'],
        password=sql_config['password']
    )

def ExecuteSQLcode(entry, fetch=False):
    global config
    config = Config()

    connect = ConnectDB(config)
    try:
        with connect:
            with connect.cursor() as cursor:
                cursor.execute(entry)
                if fetch:
                    # Fetch all results if requested
                    results = cursor.fetchall()
                    return results  # Return the fetched results
                else:
                    connect.commit()  # Commit the transaction if not fetching
    except Exception as e:
        print(f"Error executing SQL command: {e}")
        raise
    finally:
        connect.close()

#### Main
## Config
class Config():
    def __init__(self, config_file=DefaultConfigFileName):
        self.config = cfgFileCreation(config_file)

    def is_sql_enabled(self):
        return self.config["general"]["sql_enabled"]
    
    def get_sql_config(self):
        return {
            'host': self.config['sql']['hostname'],
            'database': self.config['sql']['name'],
            'user': self.config['sql']['user'],
            'password': self.config['sql']['password']
        }

## UI
class UI(Frame):
    global dictData

    def __init__(self, master):
        defFileCreation(DefaultFileName)
        cfgFileCreation(DefaultConfigFileName)

        global config
        config = Config()

        Frame.__init__(self, master)
        self.master = master
        self.DeletionToggle = BooleanVar()
        self.base_Window()

        self.editing = False
        self.current_item = None 
        self.current_column = None
        self.entry = None

        if config.is_sql_enabled():
            try:
                fetched = ExecuteSQLcode("SELECT version();")
                print(fetched)
            except Exception as err:
                messagebox.showerror("Connection Check Error", str(err))

    def base_Window(self):
        global dictData

        self.master.title(MainWindow_Title)
        self.master.geometry(MainWindow_ResWidth + "x" + MainWindow_ResHeight)
        self.master.resizable(False, False)

        if dictData:
            colAmount = len(next(iter(dictData.values())).keys()) + 1
        else:
            colAmount = 0

        def ToDatabase():
            # print(dictData)
            try:
                if config.is_sql_enabled():
                    create_table_command = """
                    CREATE TABLE IF NOT EXISTS employees (
                        name VARCHAR PRIMARY KEY,
                        occupation VARCHAR,
                        salary VARCHAR
                    )
                    """
                    ExecuteSQLcode(create_table_command)

                    ExecuteSQLcode("DELETE FROM employees")

                    for name, details in dictData.items():
                        occupation = details.get('Occupation')
                        salary = details.get('Salary')
                        sql_command = f"INSERT INTO employees (name, occupation, salary) VALUES ('{name}', '{occupation}', {salary})"
                        ExecuteSQLcode(sql_command)

                    messagebox.showinfo("Info", "Data loaded into database successfully.")
                else: messagebox.showerror("SQL disabled.")
            except Exception as e:
                messagebox.showerror("Execution Error", str(e))

        def FromDatabase():
            global dictData
            dictData = {}

            try:
                if config.is_sql_enabled():
                    select_command = "SELECT name, occupation, salary FROM employees"
                    rows = ExecuteSQLcode(select_command, fetch=True)

                    for row in rows:
                        name, occupation, salary = row
                        dictData[name] = {
                            'Occupation': occupation,
                            'Salary': salary
                        }
                    UpdateTreeView()
            except Exception as e:
                messagebox.showerror("Execution Error", str(e))

        def UpdateTreeView():
            for item in self.tree.get_children():
                self.tree.delete(item)

            for name, details in dictData.items():
                populate = [name] + [details[key] for key in details.keys()]
                self.tree.insert("", "end", values=populate)

        def createEntryANDupdate():
            # silly :3
            self.createEntry()
            UpdateTreeView()

        mainMenu = Menu(self.master, tearoff=0)
        fileMenu = Menu(mainMenu, tearoff=0)
        editMenu = Menu(mainMenu, tearoff=0)
        dbMenu = Menu(mainMenu, tearoff=0)
 
        fileMenu.add_command(label="Save", command=self.saveFile_Ask)
        fileMenu.add_command(label="Load", command=self.loadFile_Ask)
        fileMenu.add_separator()
        fileMenu.add_command(label="Settings", command=self.settings_Window)
        fileMenu.add_command(label="Exit", command=root.quit)

        editMenu.add_command(label="Add an Entry", command=createEntryANDupdate)
        editMenu.add_command(label="Refresh", command=UpdateTreeView)
        # editMenu.add_command(label="Add/Edit Columns")
        editMenu.add_separator()
        editMenu.add_checkbutton(label="Delete", onvalue=1, offvalue=0, variable=self.DeletionToggle)

        dbMenu.add_command(label=CMDWindow_Title, command=self.cmd_Window)
        dbMenu.add_separator()
        dbMenu.add_command(label="Load into Database", command=ToDatabase)
        dbMenu.add_command(label="Load from Database", command=FromDatabase)

        mainMenu.add_cascade(label="File", menu=fileMenu)
        mainMenu.add_cascade(label="Editing", menu=editMenu)
        mainMenu.add_cascade(label="Database", menu=dbMenu)

        self.master.config(menu=mainMenu)

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

    # Double click event
    def mouseDoubleClick(self, event):
        if self.editing:
            return
            
        item = self.tree.selection()
        if not item:
            return

        if self.DeletionToggle.get():
            for selected_item in item:
                name = self.tree.item(selected_item, "values")[0]
                self.tree.delete(selected_item)
                if name in dictData:
                    del dictData[name]
        else:
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

    def createEntry(self):
        global dictData

        dictData["Name"] = {
            "Occupation": "Occupation",
            "Salary": "Salary"
        }

    # def addEntry_Window(self):
    #     win = Tk()
    #     win.title(AddWindow_Title)
    #     win.geometry(AddWindow_ResWidth + "x" + AddWindow_ResHeight)
    #     win.attributes("-toolwindow", True)
    #     win.resizable(False, False)

    #     frame = ttk.Frame(win)
    #     frame.grid(padx=0, pady=0)

    #     entryName = ttk.Entry(frame)
    #     entryName.grid(row=0, column=0, sticky='NW', padx=8, pady=8)

    #     entryOcc = ttk.Entry(frame)
    #     entryOcc.grid(row=1, column=0, sticky='NW', padx=8, pady=8)

    #     entrySal = ttk.Entry(frame)
    #     entrySal.grid(row=2, column=0, sticky='NW', padx=8, pady=8)

    #     submit_button = ttk.Button(win, text="Submit", command=lambda: self.submit_entry(entryName.get(), entryOcc.get(), entrySal.get()))
    #     submit_button.grid(row=3, column=0, sticky='SE', padx=8, pady=8)

    # def submit_entry(self, name, occupation, salary):
    #     global dictData
    #     if name in dictData:
    #         messagebox.showerror("Input Error", "Name already exists.")
    #         return

    #     dictData[name] = {
    #         "Occupation": occupation,
    #         "Salary": salary
    #     }

    # def addEntry_Window(self):
    #     win = Tk()
    #     win.title(AddWindow_Title)
    #     win.geometry(AddWindow_ResWidth + "x" + AddWindow_ResHeight)
    #     win.attributes("-toolwindow", True)
    #     win.resizable(False, False)

    #     frame = ttk.Frame(win)
    #     frame.pack(padx=8, pady=8)

    #     current_height = int(AddWindow_ResHeight)

    #     def add_entry():
    #         nonlocal current_height
    #         entry = ttk.Entry(frame)
    #         entry.pack(anchor=NW, padx=8, pady=5)

    #         button = ttk.Button(frame, text="+", command=add_entry)
    #         button.pack(anchor=NE, padx=8, pady=0)

    #         current_height += 100
    #         win.geometry(AddWindow_ResWidth + "x" + str(current_height))

    #     add_entry()

    #     submit_button = ttk.Button(win, text="Submit", command=lambda: self.handle_entries(frame))
    #     submit_button.pack(anchor=SE, padx=8, pady=8)

    # def handle_entries(self, frame):
    #     entries = frame.winfo_children()
    #     data = []
    #     for widget in entries:
    #         if isinstance(widget, ttk.Entry):
    #             data.append(widget.get())
        
    #     print(data)

    #     frame.master.destroy()

    def settings_Window(self):
        global config

        win = Tk()
        win.title(SettingsWindow_Title)
        win.geometry(SettingsWindow_ResWidth + "x" + SettingsWindow_ResHeight)
        win.attributes("-toolwindow", True)
        win.resizable(False, False)

        # Initialize toggleSQL_var with the current value from the config
        toggleSQL_var = BooleanVar(value=config.is_sql_enabled())

        def save_settings():
            hostname = Hostname_entry.get()
            dbname = DBname_entry.get()
            username = Username_entry.get()
            password = Password_entry.get()
            sql_enabled = toggleSQL_var.get()

            formatted = {
                "general": {"sql_enabled": sql_enabled},
                "sql": {"hostname": hostname, "name": dbname, "user": username, "password": password},
            }

            print(formatted)

            with open("config.json", "w") as file:
                string = json.dumps(formatted, ensure_ascii=False, indent=4)
                file.write(string)

            # Recreate the config object to reflect the new settings
            global config
            config = Config()

        def defcfg():
            defFileCreation(DefaultFileName)

        defcfg_button = Button(win, text="Recreate Default File", command=defcfg)
        defcfg_button.grid(row=0, column=0, sticky='n')

        toggleSQL_checkbox = Checkbutton(win, text="SQL Enabled", variable=toggleSQL_var)
        toggleSQL_checkbox.grid(row=15, column=0, sticky='w')

        Hostname_label = Label(win, text="Hostname: ")
        Hostname_label.grid(row=20, column=0, sticky='w')

        Hostname_entry = Entry(win)
        Hostname_entry.grid(row=20, column=2, sticky='w')

        DBname_label = Label(win, text="Database: ")
        DBname_label.grid(row=25, column=0, sticky='w')

        DBname_entry = Entry(win)
        DBname_entry.grid(row=25, column=2, sticky='w')

        Username_label = Label(win, text="User: ")
        Username_label.grid(row=30, column=0, sticky='w')

        Username_entry = Entry(win)
        Username_entry.grid(row=30, column=2, sticky='w')

        Password_label = Label(win, text="Password: ")
        Password_label.grid(row=35, column=0, sticky='w')

        Password_entry = Entry(win)
        Password_entry.grid(row=35, column=2, sticky='w')

        Apply_button = Button(win, text="Apply", command=save_settings)
        Apply_button.grid(row=50, column=0, sticky='sw')

    def cmd_Window(self):
        global config

        win = Tk()
        win.title(CMDWindow_Title)
        win.geometry(CMDWindow_ResWidth + "x" + CMDWindow_ResHeight)
        win.attributes("-toolwindow", True)
        win.resizable(False, False)

        def clear():
            entryline.delete('1.0', END)

        def execute():
            receive=entryline.get("1.0","end-1c") 
            try:
                if config.is_sql_enabled():
                    exec = ExecuteSQLcode(receive)

                    if exec:
                        messagebox.showinfo("Info", str(exec))
            except Exception as e:
                messagebox.showerror("Execution Error", str(e))

        entryline = Text(win)
        entryline.grid(row=0, column=0, sticky='nsew', padx=8, pady=8)

        if config.is_sql_enabled():
            warntext = "Ready"
            text_color = "green"
            entryline.config(state="normal")
        else:
            warntext = "Unavailable"
            text_color = "red"
            entryline.config(state="disabled")

        warn_label = Label(win, text=warntext, fg=text_color, font=("Consolas", 20))
        warn_label.grid(row=1, column=0, sticky='s', padx=6, pady=6)

        clear_button = ttk.Button(win, text="Clear", command=clear)
        clear_button.grid(row=1, column=0, sticky='se', padx=6, pady=6)
        
        exec_button = ttk.Button(win, text="Execute", command=execute)
        exec_button.grid(row=1, column=0, sticky='sw', padx=6, pady=6)
        
        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)

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
