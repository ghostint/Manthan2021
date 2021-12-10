from sys import argv

f = open(argv[1], "r")
f = f.readlines()

f = [x.split("\n")[0] for x in f]
for a in f:
    print(a.lower())


