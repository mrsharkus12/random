char = "*"

height = 0
x = 0

height = int(input())

while x < height:
    print(char * height, end="")
    print("")
    height -= 1
 