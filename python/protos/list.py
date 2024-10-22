# list = [[1,222,2,2543,3,6,5,5], [4,5,1236,4,21212,3,4,3], [7,2,5,439,442,5,3,4]]
list = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

list_temp = []
for l in list:
    list_temp.extend(l)
max_size = len(str(max(list_temp)))

def drawList(list, maxSize):
    n = 0

    for i in list:
        print("|",end="")
        s = '|'.join(f"{str(x):{maxSize}}" for x in list[n])
        print(s,end='|\n')
        print("-"*(len(s) + 2))
        n+=1

drawList(list, max_size)

column = int(input())
row = int(input())
num = int(input())