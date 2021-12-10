#!/bin/python3

# Tool for getting INTERSECTION WORDS

from sys import argv
from os import listdir
from nltk import word_tokenize
import sys
import os

fold1, fold2 = argv[1], argv[2] # list of dirs to check for intersection words

def getFileTokens(file):
    f = open(file, "r")
    f = f.readlines()
    f = [x.split("\n")[0] for x in f]

    tokens = []
    for line in f:
        tok = word_tokenize(line)
        tokens += tok
    
    return tokens



def getFolderTokens(folder):
    files = listdir(folder)
    folder_tokens = []
    for f in files:
        folder_tokens += getFileTokens(folder+f)
    return folder_tokens


if os.path.isfile(fold1) and os.path.isfile(fold2):
    fold1_toks = set(getFileTokens(fold1))
    fold2_toks = set(getFileTokens(fold2)) 
else:
    fold1_toks = set(getFolderTokens(fold1))
    fold2_toks = set(getFolderTokens(fold2))

query = argv[3]

if query == "aib":
    l = list(fold1_toks.intersection(fold2_toks))
    for x in l:
        print(x)
elif query == "a-b":
    l = (fold1_toks-fold2_toks)
    for x in l:
        print(x)
elif query == "b-a":
    l = (fold2_toks-fold1_toks)
    for x in l:
        print(x)