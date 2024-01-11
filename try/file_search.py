def findFile():
    try:
        global file
        file = open(input("\nWhat is the file name?\n=> "))
    except:
        print("\nThere is no such file in this directory.")
        findFile()


findFile()

find = input("\nwhat do you wanna find?\n=> ")

print("\nwhat is the position of", find +
      " in the line?\n 1. First\n 2. Last\n 3. Any Where")


def mainTask():
    task = input("Enter [f/l/a]: ")

    global find
    count = 0

    if task == "f":
        for word in file:
            word = word.rstrip()
            if word.startswith(find):
                print(word)
                count += 1

    elif task == "l":
        for word in file:
            word = word.rstrip()
            if word.endswith(find):
                print(word)
                count += 1

    elif task == "a":
        for word in file:
            word = word.rstrip()
            if find in word:
                print(word)
                count += 1

    else:
        mainTask()

    return count


print("\nThere are", mainTask(), "line[s] that have", find, "in it.")
