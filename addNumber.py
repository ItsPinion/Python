file = open("../Canvas/balls/balls.js","r")

print(file)

sum = 0

for line in file:
    for letter in line:
        try:
            sum = sum + int(letter)
            print(letter)
        except:
            continue
print(sum)