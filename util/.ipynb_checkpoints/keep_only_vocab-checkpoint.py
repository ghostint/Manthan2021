#!/bin/python

from sys import argv

if len(argv) < 3:
    print("python3 keep_ony_vocab.py fileToClean.txt wordlist.txt")
    exit()

f = argv[1]
wordlist = argv[2]

f = open(f, "r")
f = f.readlines()[0]
wordlist = open(wordlist, "r")
wordlist = wordlist.readlines()


wl = [x.split("\n")[0] for x in wordlist]
# print(len(wl))
# print(wl)
f = f.split(" ")
# print(f"Before: {len(f)}")
f = [x for x in f if x in wl]
# print(f"After: {len(f)}")
f = " ".join(f)
print(f)

# print(f)