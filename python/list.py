list = [[1,2,2,2543,3,6,5,5], [4,5,6,4,21212,3,4,3], [7,2,5,9,442,5,3,4]]
n = 0
a = []

list_temp = []
for l in list:
    list_temp.extend(l)
max_size = len(str(max(list_temp)))
# print(list_temp)
# quit()

# for i in list:
#     s=len(list[1[n]])
# #     n+=1
# print(len(list[1[0]]))
# quit()

list1 = len(''.join(str(x) for x in list[0]))
list2 = len(''.join(str(x) for x in list[1]))
list3 = len(''.join(str(x) for x in list[2]))

if list1<=list2: a=list2
elif list2<=list3: a=list3
else: a=list1

for i in list:
    print("|",end="")
    s = '|'.join(f"{str(x):{max_size}}" for x in list[n])
    print(s,end='|\n')
    print("-"*(len(s) + 2))
    n+=1