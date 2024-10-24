import os

print("Welcome!")

# Define possible math operations
def add(x, y):
   return x + y

def subtract(x, y):
   return x - y

def mult(x, y):
   return x * y

def divide(x, y):
   return x / y

# Do a continuous loop until user decides to break it
while True:
    print("Enter 1st digit.")
    a = int(input())
    print("Enter operator.")
    operator = input()
    print("Enter 2nd digit.")
    b = int(input())

    if operator == "+":
        result = add(a,b)
    elif operator == "-":
        result = subtract(a,b)
    elif operator == "*":
        result = mult(a,b)
    elif operator == "/":
        result = divide(a,b)
    else:
        result = "Wrong operator!"

    print("--- Result ---")
    print(a, operator, b)
    print("=")
    print(result)

    print("Enter 'exit' to exit, press enter to continue.")
    exit = str(input())
    if exit == "exit":
        print("--- Exiting... ---")
        break

    print("Welcome back!")