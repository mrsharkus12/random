def drawList(list, maxSize):
    n = 0
    for i in list:
        print("|", end="")
        s = '|'.join(f"{str(x):{maxSize}}" for x in list[n])
        print(s, end='|\n')
        print("-" * (len(s) + 2))
        n += 1
def checkWin(list):
    ## P1
    if list[0][0] == "X" and list[0][1] == "X" and list[0][2] == "X":
        print("p1 win")
        return True
    if list[1][0] == "X" and list[1][1] == "X" and list[1][2] == "X":
        print("p1 win")
        return True
    if list[2][0] == "X" and list[2][1] == "X" and list[2][2] == "X":
        print("p1 win")
        return True
    
    if list[0][0] == "X" and list[1][0] == "X" and list[2][0] == "X":
        print("p1 win")
        return True
    if list[0][1] == "X" and list[1][1] == "X" and list[2][1] == "X":
        print("p1 win")
        return True
    if list[0][2] == "X" and list[1][2] == "X" and list[2][2] == "X":
        print("p1 win")
        return True
    
    if list[0][0] == "X" and list[1][1] == "X" and list[2][2] == "X":
        print("p1 win")
        return True
    if list[0][2] == "X" and list[1][1] == "X" and list[2][0] == "X":
        print("p1 win")
        return True
    
    ## P2
    if list[0][0] == "O" and list[0][1] == "O" and list[0][2] == "O":
        print("p2 win")
        return True
    if list[1][0] == "O" and list[1][1] == "O" and list[1][2] == "O":
        print("p2 win")
        return True
    if list[2][0] == "O" and list[2][1] == "O" and list[2][2] == "O":
        print("p2 win")
        return True
    
    if list[0][0] == "O" and list[1][0] == "O" and list[2][0] == "O":
        print("p2 win")
        return True
    if list[0][1] == "O" and list[1][1] == "O" and list[2][1] == "O":
        print("p2 win")
        return True
    if list[0][2] == "O" and list[1][2] == "O" and list[2][2] == "O":
        print("p2 win")
        return True
    
    if list[0][0] == "O" and list[1][1] == "O" and list[2][2] == "O":
        print("p2 win")
        return True
    if list[0][2] == "O" and list[1][1] == "O" and list[2][0] == "O":
        print("p2 win")
        return True
def checkDraw(list):
    for sublist in list:
        if '-' in sublist:
            return False
    print("draw")
    return True

rows = 3
cols = 3

list = [["-" for _ in range(cols)] for _ in range(rows)]

while True:
    Player1Action = True
    Player2Action = False

    drawList(list, 0)

    checkDraw(list)
    draw = checkDraw(list)
    checkWin(list)
    win = checkWin(list)

    if draw: break
    if win: break

    while Player1Action:
        try:
            print("player1")
            row = int(input(f"Enter the row (0 to {rows - 1}): "))
            col = int(input(f"Enter the column (0 to {cols - 1}): "))

            if 0 <= row < rows and 0 <= col < cols:
                list[row][col] = "X"
                Player1Action = False
                Player2Action = True
            else:
                print(f"Error!! Invalid row or column.")
        except ValueError:
            print("error!!!")

    drawList(list, 0)

    checkDraw(list)
    draw = checkDraw(list)
    checkWin(list)
    win = checkWin(list)

    if draw: break
    if win: break

    while Player2Action:
        try:
            print("player2")
            row = int(input(f"Enter the row (0 to {rows - 1}): "))
            col = int(input(f"Enter the column (0 to {cols - 1}): "))
            
            if 0 <= row < rows and 0 <= col < cols:
                list[row][col] = "O"
                Player1Action = True
                Player2Action = False
            else:
                print(f"Error!! Invalid row or column.")
        except ValueError:
            print("error!!!")
