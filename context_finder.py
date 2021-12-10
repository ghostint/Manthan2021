from models.topics_lda import TopicModel
from cleanser.cleaner import Cleaner

class ContextFinder:
    def __init__(self, num_topics=30, passes=10):
        ## Paths to data folder ##
        ## Set using setters ##
        self.__bjp = None
        self.__congress = None
        
        self.__islam =  None 
        self.__hindus =  None 
        self.__sikhs =  None 

        self.__extremism = None



        self.bjp_model = None
        self.congress_model = None

        self.islam_model = None
        self.hindus_model = None
        self.sikhs_model = None

        self.extremism = None


        ## Model hyperparameters.
        self.n_topics = num_topics
        self.passes = passes ## TODO: needed to configure passes hyper parameter


    def train(self):

        if self.__bjp is not None:
            bjp_clean = Cleaner(self.__bjp)
            bjp_clean.clean()
            self.bjp_model = TopicModel(bjp_clean.all_line_tokens, self.n_topics)



        if self.__congress is not None:
            congress_clean = Cleaner(self.__congress)
            congress_clean.clean()
            self.congress_model = TopicModel(congress_clean.all_line_tokens, self.n_topics)


        if self.__hindus is not None:
            hindus_clean = Cleaner(self.__hindus)
            hindus_clean.clean()
            self.hindus_model = TopicModel(hindus_clean.all_line_tokens, self.n_topics)



        if self.__islam is not None:
                islam_clean = Cleaner(self.__islam)
                islam_clean.clean()
                self.islam_model = TopicModel(islam_clean.all_line_tokens, self.n_topics)


        if self.__sikhs is not None:
                sikhs_clean = Cleaner(self.__sikhs)
                sikhs_clean.clean()
                self.sikhs_model = TopicModel(sikhs_clean.all_line_tokens, self.n_topics)



        if self.__extremism is not None:
                sikhs_clean = Cleaner(self.__sikhs)
                sikhs_clean.clean()
                self.sikhs_model = TopicModel(sikhs_clean.all_line_tokens, self.n_topics)



    def __predict_helper(self, text, model, thresh, type_):

        if model == None:
            return False

        bigs, trigs, single = model.predict(text)

        # TODO: Need to write code for bigs, trigs checking.
        if type_ == "single":
            outcome = [x[1] for x in single if x[1] >= thresh]
            return len(outcome) > 0

        





    ## Prediction.
    def predict(self, text, threshold=0.2, type_="single"):
        """
            @type_: <str>; valid_options: "single", "bigs", "trigs"
        """
        
        isBJP = self.__predict_helper(text, self.bjp_model, thresh=threshold, type_=type_)
        isCongress = self.__predict_helper(text, self.congress_model, thresh=threshold, type_=type_)

        isHindu = self.__predict_helper(text, self.hindus_model, thresh=threshold, type_=type_)
        isIslam = self.__predict_helper(text, self.islam_model, thresh=threshold, type_=type_)
        isSikh = self.__predict_helper(text, self.sikhs_model, thresh=threshold, type_=type_)

        isExtremist = self.__predict_helper(text, self.extremism, thresh=threshold, type_=type_)

        return {"bjp":isBJP, "congress":isCongress, "hindu":isHindu, "islam":isIslam, "sikh":isSikh, "extremist":isExtremist}


    ## Setter for instance variables.
    def set_bjp_folder(self, folder):
        self.__bjp = folder

    def set_congress_folder(self, folder):
        self.__congress = folder

    def set_hindus_folder(self, folder):
        self.__hindus = folder

    def set_islam_folder(self, folder):
        self.__islam = folder

    def set_sikh_folder(self, folder):
        self.__sikhs = folder

    def set_extremism_folder(self, folder):
        self.__extremism = folder