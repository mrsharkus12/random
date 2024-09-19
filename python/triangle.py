char = "*"
space = "0"

height = 0
x = 0

height = int(input())

while x < height:
    x += 1
    height -= 1
    print(space * height, char * x, char * x, end="")
    print("")
