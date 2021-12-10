from sys import argv

if len(argv) < 2:
    print("python3 wordlist_create.py <inputFile> <outputFile>")
    exit(0)


f = open(argv[1], "r")
f = f.readlines()

data = f[0]
data = data.split(" ")

data = list(set(data))
data.sort()

data = "\n".join(data)
out = open(argv[2], "w+")
out.writelines(data)
out.close()
