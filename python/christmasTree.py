# define characters for drawing
char = "*"
emptyChar = " "

# define trig drawing as a function
def makeTrig(height):
    # do an xtra row to avoid first empty row
    row = 1 

    while row <= height:
        # make offsets
        space = height - row  
        print(emptyChar * space, end="")

        # make 1st side
        for i in range(row):
            print(char, end="")
        
        # make 2nd side
        for i in range(row - 1):
            print(char, end="")
        
        print("")
        row += 1

# define making a christmas tree
def drawChristmasTree(layers, trunk_width, trunk_height, trunk_space):
    # 5 is good enough
    height = 5
    for i in range(layers):
        makeTrig(height)
    
    # draw the trunk of da tree
    for i in range(trunk_height):
        print(emptyChar * trunk_space + char * trunk_width)

print("Enter amount of leaves (layers) default 2")
leaves = int(input())
print("Enter the trunk's width, default 3")
width = int(input())
print("Enter trunk's height, default 2")
height = int(input())
print("Enter trunk's offset, default 3")
offset = int(input())

# drawChristmasTree(2, 3, 2, 3)
drawChristmasTree(leaves, width, height, offset)