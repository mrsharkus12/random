import json

DefaultFileName = "Default"
with open(DefaultFileName, "r", encoding='utf-8') as file:
    string = json.load(file)
    dict = string
    print(f"Successfully read {DefaultFileName}")

# dict = {
#     "workers": {
#         "vanya": {
#             "occupation": "director",
#             "wage": 420
#         },
#         "sanya": {
#             "occupation": "worker",
#             "wage": 52
#         }
#     }
# }

while True:
    dict_wawawa = dict["workers"]
    print("make selection (edit, view, delete, save)")
    sel = input()
    
    if sel == "edit":
        print(dict_wawawa)
        input1 = input("name: ")
        input2 = input("param: ")
        input3 = input("value: ")
        if input1 not in dict_wawawa:
            dict_wawawa[input1] = {}
        dict_wawawa[input1][input2] = input3
        print(f"Edited {input1}'s {input2} to {input3}")
    elif sel == "view":
        print(dict_wawawa)
    elif sel == "delete":
        print(dict_wawawa)
        input1 = input("name: ")
        if input1 not in dict_wawawa:
            print("item does not exist")
        del dict_wawawa[input1]
        print(f"Removed {input1} from dict")
    elif sel == "save":
        print('enter file name')
        fileName = input("")
        with open(fileName, "w") as file:
            string = json.dumps(dict)
            file.write(string)
        print(f"Successfully saved to {fileName}")
    elif sel == "load":
        print('enter file name')
        fileName = input("")

        with open(fileName, "r", encoding='utf-8') as file:
            string = json.load(file)
            dict = string
            print(f"Successfully read {fileName}")
            print(dict)
    else:
        print("wrong selection")