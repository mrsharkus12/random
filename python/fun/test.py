file = "la-creatura.fuck"

def readTheCreature(fileName):
    with open(fileName, "r", encoding='utf-8') as file:
        content = file.read()
    return content

result = readTheCreature(file)

print(result)