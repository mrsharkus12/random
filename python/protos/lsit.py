list = [[1,2,3,6,5,5,4,4], [4,5,6,4,21212,3,4,3], [7,8,5,9,2,5,3,4]]
n = 0

list1 = len(''.join(str(x) for x in list[0]))
list2 = len(''.join(str(x) for x in list[1]))
list3 = len(''.join(str(x) for x in list[2]))

for i in list:
    print("|",end="")
    print('|'.join(str(x) for x in list[n]))
    print("-"*list2)
    n+=1

print(list1)
print(list2)
print(list3)
print("------------")
print(''.join(str(x) for x in list[0]))
print(''.join(str(x) for x in list[1]))
print(''.join(str(x) for x in list[2]))
print("------------")
print(list1*2)
print(list2*2)
print(list3*2)