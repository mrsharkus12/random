import json

SampleDict = {
    "workers": {
        "john": {
            "occupation": "director",
            "wage": 1500
        },
    }
}

DefaultFileName = "Default"
try:
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dict = string
        # print(f"Successfully read {DefaultFileName}")
except FileNotFoundError:
    with open(DefaultFileName, "w") as file:
        string = json.dumps(SampleDict)
        file.write(string)
    # print(f"Successfully saved to {DefaultFileName}")
    with open(DefaultFileName, "r", encoding='utf-8') as file:
        string = json.load(file)
        dict = string
        # print(f"Successfully read {DefaultFileName}")

while True:
    tempDict = dict["workers"]
    print("Make a selection (edit, view, delete, save, load, end)")
    sel = input()
    sel = sel.lower().replace(" ", "")

    if sel == "edit":
        print(tempDict)
        input1 = input("Name: ")
        input2 = input("Parameter: ")
        input3 = input("Value: ")
        if input1 not in tempDict:
            tempDict[input1] = {}
        tempDict[input1][input2] = input3
        print(f"Edited {input1}'s {input2} to {input3}")
    elif sel == "view":
        print(tempDict)
    elif sel == "delete":
        print(tempDict)
        input1 = input("Name: ")
        try:
            del tempDict[input1]
            print(f"Removed {input1} from current dictionary")
        except KeyError:
            print("Item does not exist")
    elif sel == "save":
        print('Enter file name')
        fileName = input("")
        with open(fileName, "w") as file:
            string = json.dumps(dict)
            file.write(string)
        print(f"Successfully saved to {fileName}")
    elif sel == "load":
        print('Enter file name')
        fileName = input("")
        with open(fileName, "r", encoding='utf-8') as file:
            string = json.load(file)
            dict = string
            print(f"Successfully read {fileName}")
            print(dict)
    elif sel == "end":
        break
    else:
        print("Wrong selection")