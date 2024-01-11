import random

miss = 0


def find():
    global miss
    miss += 1
    try:
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        c = float(input("Enter the third number: "))
        if a > b:
            if a > c:
                print(a, "is the biggest Number.")
            else:
                print(c, "is the biggest Number.")
        else:
            if b > c:
                print(b, "is the biggest Number.")
            else:
                print(c, "is the biggest Number.")
    except:
        return find()
find()
