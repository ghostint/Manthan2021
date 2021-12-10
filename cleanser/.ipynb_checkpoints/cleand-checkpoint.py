from sys import argv
from nltk.corpus import stopwords # importing stopwords
from nltk import word_tokenize
import re
from stopwords.stops import Stops

if len(argv) < 3:
    print(("Missing required arguments"))
    print("Usage: python3 cleand.py <inputFile> <outputFile> <optional:customStopWordFile>")
    exit()

fname = argv[1] # File to be cleaned.
cfname = argv[2] # Cleaned File.


all_stops = stopwords.words("english") # Collection of all stopwords

s = Stops(path.join(getcwd(), "stopwords/")) # Adding some custom stopwords, common pronouns and verbs.
all_stops +=  s.stops 


if len(argv) == 4:
    # if external stopwords are provided add them to all_stops
    stopWordFile = argv[3]
    f = open(stopWordFile, "r")
    f = f.readlines()
    f = [x.split("\n")[0] for x in f]
    all_stops += f



# Removing puncutation marks
def remove_puncs(line):
    from string import punctuation
    punctuation.replace(".", "")
    clean = ""
    for x in range(0, len(line)):
        if line[x] == '.':
            clean += " "
        if line[x] in punctuation:
            pass
        else:
            clean += line[x]
    return clean



def clean_line(line):
    if len(line) > 0:
        line = word_tokenize(line)
        line = [word.lower() for word in line if word not in all_stops]
        line = " ".join(line)
        
        return remove_puncs(line)


## Opening file for reading mode. 
f = argv[1] # filename to be cleaned.
f = open(fname, "r")
f = f.readlines()
### END ###

f = [clean_line(line) for line in f] # Cleaning each line in the file.

### Writing to clean file.
cf = open(cfname, "w+")
cf.writelines(f)
cf.close()
print("Cleaned data saved in ", cfname)
### 


