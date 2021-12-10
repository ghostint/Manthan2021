import twint
import pandas as pd
import os
import re
import nltk 
import itertools
import emoji
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def load_dict_smileys():
    
    return {
        ":‑)":"smiley",
        ":-]":"smiley",
        ":-3":"smiley",
        ":->":"smiley",
        "8-)":"smiley",
        ":-}":"smiley",
        ":)":"smiley",
        ":]":"smiley",
        ":3":"smiley",
        ":>":"smiley",
        "8)":"smiley",
        ":}":"smiley",
        ":o)":"smiley",
        ":c)":"smiley",
        ":^)":"smiley",
        "=]":"smiley",
        "=)":"smiley",
        ":-))":"smiley",
        ":‑D":"smiley",
        "8‑D":"smiley",
        "x‑D":"smiley",
        "X‑D":"smiley",
        ":D":"smiley",
        "8D":"smiley",
        "xD":"smiley",
        "XD":"smiley",
        ":‑(":"sad",
        ":‑c":"sad",
        ":‑<":"sad",
        ":‑[":"sad",
        ":(":"sad",
        ":c":"sad",
        ":<":"sad",
        ":[":"sad",
        ":-||":"sad",
        ">:[":"sad",
        ":{":"sad",
        ":@":"sad",
        ">:(":"sad",
        ":'‑(":"sad",
        ":'(":"sad",
        ":‑P":"playful",
        "X‑P":"playful",
        "x‑p":"playful",
        ":‑p":"playful",
        ":‑Þ":"playful",
        ":‑þ":"playful",
        ":‑b":"playful",
        ":P":"playful",
        "XP":"playful",
        "xp":"playful",
        ":p":"playful",
        ":Þ":"playful",
        ":þ":"playful",
        ":b":"playful",
        "<3":"love"
        }


def load_dict_contractions():
    
    return {
        "ain't":"is not",
        "amn't":"am not",
        "aren't":"are not",
        "can't":"cannot",
        "'cause":"because",
        "couldn't":"could not",
        "couldn't've":"could not have",
        "could've":"could have",
        "daren't":"dare not",
        "daresn't":"dare not",
        "dasn't":"dare not",
        "didn't":"did not",
        "doesn't":"does not",
        "don't":"do not",
        "e'er":"ever",
        "em":"them",
        "everyone's":"everyone is",
        "finna":"fixing to",
        "gimme":"give me",
        "gonna":"going to",
        "gon't":"go not",
        "gotta":"got to",
        "hadn't":"had not",
        "hasn't":"has not",
        "haven't":"have not",
        "he'd":"he would",
        "he'll":"he will",
        "he's":"he is",
        "he've":"he have",
        "how'd":"how would",
        "how'll":"how will",
        "how're":"how are",
        "how's":"how is",
        "I'd":"I would",
        "I'll":"I will",
        "I'm":"I am",
        "I'm'a":"I am about to",
        "I'm'o":"I am going to",
        "isn't":"is not",
        "it'd":"it would",
        "it'll":"it will",
        "it's":"it is",
        "I've":"I have",
        "kinda":"kind of",
        "let's":"let us",
        "mayn't":"may not",
        "may've":"may have",
        "mightn't":"might not",
        "might've":"might have",
        "mustn't":"must not",
        "mustn't've":"must not have",
        "must've":"must have",
        "needn't":"need not",
        "ne'er":"never",
        "o'":"of",
        "o'er":"over",
        "ol'":"old",
        "oughtn't":"ought not",
        "shalln't":"shall not",
        "shan't":"shall not",
        "she'd":"she would",
        "she'll":"she will",
        "she's":"she is",
        "shouldn't":"should not",
        "shouldn't've":"should not have",
        "should've":"should have",
        "somebody's":"somebody is",
        "someone's":"someone is",
        "something's":"something is",
        "that'd":"that would",
        "that'll":"that will",
        "that're":"that are",
        "that's":"that is",
        "there'd":"there would",
        "there'll":"there will",
        "there're":"there are",
        "there's":"there is",
        "these're":"these are",
        "they'd":"they would",
        "they'll":"they will",
        "they're":"they are",
        "they've":"they have",
        "this's":"this is",
        "those're":"those are",
        "'tis":"it is",
        "'twas":"it was",
        "wanna":"want to",
        "wasn't":"was not",
        "we'd":"we would",
        "we'd've":"we would have",
        "we'll":"we will",
        "we're":"we are",
        "weren't":"were not",
        "we've":"we have",
        "what'd":"what did",
        "what'll":"what will",
        "what're":"what are",
        "what's":"what is",
        "what've":"what have",
        "when's":"when is",
        "where'd":"where did",
        "where're":"where are",
        "where's":"where is",
        "where've":"where have",
        "which's":"which is",
        "who'd":"who would",
        "who'd've":"who would have",
        "who'll":"who will",
        "who're":"who are",
        "who's":"who is",
        "who've":"who have",
        "why'd":"why did",
        "why're":"why are",
        "why's":"why is",
        "won't":"will not",
        "wouldn't":"would not",
        "would've":"would have",
        "y'all":"you all",
        "you'd":"you would",
        "you'll":"you will",
        "you're":"you are",
        "you've":"you have",
        "Whatcha":"What are you",
        "luv":"love",
        "sux":"sucks"
        }




class TwitterProfile:
    
    def __init__(self, username):
        self.username = username
        self._c = twint.Config()
        self._c.Username = username
        self._c.Store_csv = True
        self._c.limit = 4000
        self.filepath =  os.path.join(os.getcwd(), f"model_data/target_users/twitter/{username}.csv")
        self.filepath_clean = os.path.join(os.getcwd(), f"model_data/target_users/twitter/{username}_clean.csv")
        self.filepath_clean_txt = os.path.join(os.getcwd(), f"model_data/target_users/twitter/{username}_clean.txt")
        self._c.Output = self.filepath
        self._c.Profile_full = True
        self._c.Debug = False
        self._c.Hide_output = True
        self.fetch_success = True
        self._c.Since = "2020-01-01"
        self.dataExists = os.path.exists(self.filepath)
        self.cleanDataExists = os.path.exists(self.filepath_clean)
        

    @staticmethod
    def remove_content(text):
        text = re.sub(r"http\S+", "", text) #remove urls
        text=re.sub(r'\S+\.com\S+','',text) #remove urls
        text=re.sub(r'\@\w+','',text) #remove mentions
        text =re.sub(r'\#\w+','',text) #remove hashtags
        
        CONTRACTIONS = load_dict_contractions()
        words = text.split()
        reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
        text = ' '.join(reformed)
        
        text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
        
        SMILEY = load_dict_smileys()  
        words = text.split()
        reformed = [SMILEY[word] if word in SMILEY else word for word in words]
        text = " ".join(reformed)
    
        #Deal with emojis
        text = emoji.demojize(text)

        text = text.replace(":"," ")
        text = ' '.join(text.split())
        text = text.strip()
        # res = TwitterProfile.translate_text(text, dest="en")
        # res = translator.translate(text, dest="en")
        return text
    
    
    
    @staticmethod
    def process_text(text, stem=False, lang='en', stopw=True):
        if text == " ":
            return text
        stemmer = PorterStemmer()
        text = TwitterProfile.remove_content(text);
        stop_words = set(stopwords.words("english"))
        text = re.sub('[^A-Za-z]', ' ', text.lower()) #remove non-alphabets
        tokenized_text = word_tokenize(text) #tokenize
        if stopw:
            tokenized_text  = [
                word for word in tokenized_text
                if word not in stop_words
            ]
             
        if stem:
            tokenized_text=[stemmer.stem(word) for word in tokenized_text]

        text = ' '.join(tokenized_text)  
        
        return text
        
        
    
            

    def _get_df(self):
        if self.fetch_success:
            # from ..extract_text_image.extractor import ExtractTextFromImage
            # import validators
            data = pd.read_csv(self.filepath);
            columns = [ "tweet","language", 'image_text']
            data['tweet'] = data['tweet'].apply(lambda x : TwitterProfile.process_text(x))
            
            ## Image text extraction happening here ##
            # col = []
            # for images in data['photos']:
            #     row = []
                
            #     images = images.replace('[', '')
            #     images = images.replace(']','')
                
            #     urls = images.split(',')
            #     for url in urls:
            #         url = url.replace("'",'')
            #         print(url)
            #         if validators.url(url):
            #             img = ExtractTextFromImage(url)
            #             row += img.get()
                    
            #     col.append(row)
                
            # data['image_text'] = col

            ### END ####
                
            cleaned_data = data.filter(columns, axis=1)
            return cleaned_data
        return None


    def save_clean(self):
        if not self.cleanDataExists:
            data = self._get_df();
            data = data.dropna()
            data.to_csv(self.filepath_clean, encoding="utf-8")
            
        return self.filepath_clean
            
    def clear(self):
        if os.path.exists(self.filepath):
            self.dataExists = False
            os.remove(self.filepath)
        if os.path.exists(self.filepath_clean):
            self.cleanDataExists = False
            os.remove(self.filepath_clean)

    def get(self):
        if self.dataExists:
            return self.filepath
        
        twint.run.Profile(self._c)
        return self.filepath

    def df(self):
        data = pd.read_csv(self.filepath_clean)
        data = data.dropna()
        return data
        



if __name__ == "__main__":
    p = TwitterProfile("indfoundation")
    p.get()
    p.save_clean();
    data = p.df();
    

