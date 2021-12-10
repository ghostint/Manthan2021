import nltk
import sklearn.feature_extraction.text as txt
import os

from nltk.corpus import stopwords
from nltk.util import ngrams
from string import punctuation
from os import path, getcwd


class Stops:
    def __init__(self, d):
        self.stops = []
        self.d = d
        self.__load(self.d)
    def __load(self, d):
        from os import getcwd, listdir
        files = [x for x in listdir(d) if x.endswith(".txt")]
        for f in files:
            ff = open(d+f, "r")
            ff = ff.readlines()
            data = [d.split("\n")[0] for d in ff]
            self.stops += data

class Cleaner:
    def __init__(self, work_dir):
        self.wd = work_dir

        self.nouns_ = []
        self.adjs_ = []
        self.named_ents_ = []

        self.tfid_features_ = []
        self.lda_features = []


        self.__stops  = stopwords.words("english")
        self.__stops += list(punctuation)
        self.__stops.append("`")

        self.custom_stops = Stops(path.join(getcwd(), "cleanser/stopwords/"))
        self.__stops += self.custom_stops.stops

    
        self.__puncs = list(punctuation)
        self.__puncs.append(".")
        self.__puncs.append("-")

        self.all_tokens = [] # list holding all the tokens.
        self.all_lines = [] # list holding all the lines.
        self.all_line_tokens = [] # list holding tokens of every line

        self.__pos_tagged = []

    def clean(self):
        """ To clean the whole directory.. """
        
        files = self.getFiles()
        #print("Available Files: ",files)
        #print(self.cleanFile(files[0]))

        lines = []
        for f in files:
            for line in self.cleanFile(f):
                lines.append(line)
        lines = list(set(lines))
        

        self.all_lines = lines
        
        #self.all_tokens = (self.all_tokens)
    
        self.__posTag()
        self.__extracNouns()
        self.__extractAdjs()        
    



    def __extracNouns(self):
        self.nouns_ = [x[0] for x in self.__pos_tagged if "N" in x[1]]
        

    def __extractAdjs(self):
        self.adjs_ = [x[0] for x in self.__pos_tagged if "J" in x[1]]

    def __extractNEs(self):
        self.named_ents_ = nltk.chunk.named_entity

    def __posTag(self):
        self.__pos_tagged = nltk.pos_tag(self.all_tokens)


    def cleanFile(self, f):

        """ Returns a list of cleaned lines from the f file """
        lines = self.readFile(f) # extracting the lines from the file.

        cleaned_lines = []
        for line in lines:
            
            for p in self.__puncs:
                for i in range(line.count(p)):
                    line.replace(p,"")

            line_tokens = nltk.word_tokenize(line)
            filtered_tokens = self.filterTokens(line_tokens)
            new_line = " ".join(filtered_tokens)
            cleaned_lines.append(new_line)
    
        return cleaned_lines
        

    @staticmethod
    def removeStops(cls, tokens):
        return [x for x in tokens if x not in self.__stops]

    
    def filterTokens(self, tokens):
        """ Returns filtered tokens, by removing numerics, lowercasing tokens, removing stops.. """
       

        # Lowercasing.
        ftokens = [x.lower() for x in tokens]

        # Removing numerics
        ftokens = [x for x in ftokens if not x.isnumeric()]

        # Removing stops.
        ftokens = [x for x in ftokens if x not in self.__stops]

        # Only taking words, containing chars more than 1
        ftokens = [x for x in ftokens if len(x) > 2]
        
        # Lemmatizing.
        #lemma = nltk.WordNetLemmatizer()
        #ftokens = [lemma.lemmatize(tok, "v") for tok in ftokens]

        # Stemming
        #stemmer = nltk.SnowballStemmer("english")
        #ftokens = [stemmer.stem(tok) for tok in ftokens]
        
        bigrams = ngrams(ftokens, 2)
        trigrams = ngrams(ftokens, 3)

        bigrams = [list(x) for x in bigrams]
        trigrams = [list(x) for x in trigrams]

        fftokens = Cleaner.getNouns(" ".join(ftokens))
        fftokens = list(set(fftokens))
        


        self.all_line_tokens.append(fftokens)
        
        for x in bigrams:
            self.all_line_tokens.append(x)

        for x in trigrams:
            self.all_line_tokens.append(x)

        self.all_tokens += ftokens
        return ftokens
        

    def getFiles(self):
        """ Returns the list of files in the working dir. """
        files = os.listdir(self.wd)
        return [self.wd+f for f in files if f.startswith("clean_")]
        
    
    def readFile(self, path):
        """ Returns the list of lines from the file. """
        f = open(path, "r")
        f = f.readlines()
        return f

    # def lda(self):
    #     from gensim.test.utils import common_texts
    #     from gensim.corpora.dictionary import Dictionary
    #     from gensim.models import LdaModel
        
    #     comm_dict = Dictionary(self.all_line_tokens)
    #     #print(list(comm_dict.items()))
    #     common_corpus = [comm_dict.doc2bow(text) for text in self.all_line_tokens]


    #     ld = LdaModel(common_corpus, num_topics=10)

    #     unseen = ["bjp", "rss", "sangh"]
        
    #     unseen = comm_dict.doc2bow(unseen)

    #     print(ld.print_topics())
        
    @classmethod
    def getNouns(ctx, raw_line):
        tokens = nltk.word_tokenize(raw_line)
        pos = nltk.pos_tag(tokens)
        return [x[0] for x in pos if "NN" in x[1]]

    @classmethod
    def getAdjs(ctx, raw_line):
        tokens = nltk.word_tokenize(raw_line)
        pos = nltk.pos_tag(tokens)

        return [x[0] for x in pos if "JJ" == x[1]]






if __name__ == "__main__":
    
    cleaner = Cleaner("/media/hdd/home/ghostin/Documents/Codes/Manthan/data/model_data/hindus/")
    cleaner.clean()
    print(cleaner.all_line_tokens[:20])
    
    # cleaner.lda()










