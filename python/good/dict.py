import json

SampleDict = {"john": {"occupation": "director", "wage": 1500}}
DefaultFileName = "Default.json"

try:
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dict = string
        # print(f"Successfully read {DefaultFileName}")
except FileNotFoundError:
    # create a sample file
    with open(DefaultFileName, "w") as file:
        string = json.dumps(SampleDict)
        file.write(string)
    # print(f"Successfully saved to {DefaultFileName}")
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dict = string
        # print(f"Successfully read {DefaultFileName}")

while True:
    try:
        tempDict = dict
    except TypeError:
        print("Fatal error!!! pls restart")
        break

    print("Make a selection (Edit, View, Delete, Save, Load, End)")
    sel = input()
    sel = sel.lower().replace(" ", "")

    if sel == "edit" or sel == "e":
        editType = ""
        print(tempDict)
        name = input("Name: ")
        param = input("Parameter: ")
        val = input("Value: ")
        if name not in tempDict:
            tempDict[name] = {}
            editType = "Added"
        else:
            editType = "Edited"
        tempDict[name][param] = val
        print(f"{editType} {name}'s {param} to {val}")
    elif sel == "view" or sel == "v":
        print(tempDict)
    elif sel == "delete" or sel == "d" or sel == "del":
        print(tempDict)
        name = input("Name: ")
        try:
            del tempDict[name]
            print(f"Removed {name} from current dictionary")
        except KeyError:
            print("Item does not exist")
    elif sel == "save" or sel == "s":
        print('Enter file name')
        fileName = input("")
        if not fileName.endswith('.json'):
            fileName = fileName + ".json"
        try:
            with open(fileName, "w") as file:
                string = json.dumps(dict)
                file.write(string)
            print(f"Successfully saved to {fileName}")
        except OSError:
            print("Invalid character used")
    elif sel == "load" or sel == "l":
        print('Enter file name')
        fileName = input("")
        if not fileName.endswith('.json'):
            fileName = fileName + ".json"
        try:
            with open(fileName, "r", encoding='utf-8') as file:
                string = json.load(file)
                dict = string
                print(f"Successfully read {fileName}")
                print(dict)
        except FileNotFoundError:
            print("File not found")
    elif sel == "end" or sel == "exit":
        break
    else:
        print("Wrong selection")