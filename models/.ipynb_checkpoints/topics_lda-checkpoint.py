import nltk
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel

from cleanser.cleaner import Cleaner

from nltk import word_tokenize
from collections import defaultdict
from nltk.util import ngrams
from nltk.corpus import stopwords

from cleanser.cleaner import Stops

from os import path, getcwd


class TopicModel:
    """ 
        TopicModel can be used to extract topic of the line using LDA.
        predict: method can be used to determine the liklihood of tokened_line to belong to current category.
    """

    def __init__(self, all_line_tokens, num_topics):
        
        self.tokened_lines = all_line_tokens
        self.d = Dictionary(self.tokened_lines) # global dictionary.
        self.bow = [self.d.doc2bow(line) for line in self.tokened_lines]
        
        self.stops = stopwords.words("english")
        ## Adding additional stopwords ##
        # self.cstop = Stops(path.join(getcwd(), "/cleanser/stopwords/"))
        # self.stops += self.cstop.stops
        ## Additing additional stopwords ##

        self.n = num_topics
        self.__model = None
        self.__train()
        
    
    def __train(self):
        self.__model = LdaModel(self.bow, self.n, passes=100, id2word=self.d,chunksize=200)
    
        
    def __predict(self, tokened_line):
        bow_of_line = self.d.doc2bow(tokened_line)
        return self.__model.get_document_topics(bow_of_line)


    def predict(self, line):
        line = line.lower()
        word_tokens = word_tokenize(line)

        word_tokens = [x for x in word_tokens if x not in self.stops]

        bigrams = ngrams(word_tokens, 2)
        trigrams = ngrams(word_tokens, 3)

        nouns = Cleaner.getNouns(line)
        adjs = Cleaner.getAdjs(line)


        noun_adjs = nouns + adjs

       


        bigs = [self.__predict(list(x)) for x in bigrams]
        trigs = [self.__predict(list(x)) for x in trigrams]
        third = self.__predict(noun_adjs)

        return [bigs, trigs, third]
      

    def getModel(self):
        return self.__model
