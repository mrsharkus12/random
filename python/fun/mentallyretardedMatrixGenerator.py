# import os

## input check
def stupidCheck(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0: return value
            else: print("idiot!! do NOT enter negatives!!!!!!")
        except ValueError: print("error!!!!")

## matrix drawing
def drawList(list, maxSize):
    n = 0
    for i in list:
        print("|", end="")
        s = '|'.join(f"{str(x):{maxSize}}" for x in list[n])
        print(s, end='|\n')
        print("-" * (len(s) + 2))
        n += 1

# list = [[1,222,2,2543,3,6,5,5], [4,5,1236,4,21212,3,4,3], [243,2,5,439,442,5,3,4]]
# print = drawList(list)

## matrix saving
def saveToFile(list, maxSize, fileName):
    with open(fileName, "w") as file:
        n = 0
        for i in list:
            s = '|'.join(f"{str(x):{maxSize}}" for x in list[n])
            file.write("|" + s + "|\n")
            file.write("-" * (len(s) + 2) + "\n")
            n += 1
        # file.write("\n")
    print(f"Successfully saved to {fileName}")

rows = stupidCheck("Enter the number of rows: ")
cols = stupidCheck("Enter the number of columns: ")

list = [[0 for _ in range(cols)] for _ in range(rows)]

## getmaxsize of a matrix
def getMaxSize(list):
    list_temp = []
    for l in list: list_temp.extend(l)
    return len(str(max(list_temp)))

# dividerLenght = 15

while True:
    max_size = getMaxSize(list)

    print("\nPreview:")
    drawList(list, max_size)
    # print("=" * dividerLenght)

    edit = input("Edit a cell? (Y/N): ").strip().lower()
    if edit != 'y': break

    ## implement silly check
    try:
        row = int(input(f"Enter the row (0 to {rows - 1}): "))
        col = int(input(f"Enter the column (0 to {cols - 1}): "))

        if 0 <= row < rows and 0 <= col < cols:
            new_value = int(input(f"Enter the new value for cell ({row}, {col}): "))
            list[row][col] = new_value
        else:
            print(f"Error!! Invalid row or column.")
    except ValueError:
        print("error!!!")

print("\nFinal:")
drawList(list, max_size)
# print("=" * dividerLenght)

def readSecret():
    secretfile = "la-creatura"
    ## 23:39 type shiii
    with open(secretfile, "r", encoding='utf-8') as file:
        content = file.read()
    return content
secretresult = readSecret()

askSave = input("Save? (Y/N): ").strip().lower()
if askSave == 'y':
    name = input("Filename: ").strip()
    saveToFile(list, max_size, name)
if askSave == 'neco':
    print(secretresult)

## wawawawawa
