from flask import *
import flask

import logging
from scrapers.twitter.twitter_profile import TwitterProfile
from threading import Thread, Lock  
from os import getcwd, path
import matplotlib.pyplot as plt
import nest_asyncio
nest_asyncio.apply()


lock = Lock()


from context_finder import ContextFinder
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle


# finder = ContextFinder()
# finder.set_bjp_folder("model_data/bjp/")
# finder.set_congress_folder("model_data/congress/")
# finder.set_hindus_folder("model_data/hindus/")
# finder.set_islam_folder("model_data/islam/")
# finder.set_sikh_folder("model_data/sikhs/")
# finder.train()

f = open("finder.pkl","rb") # TODO: reading pickle model instead of training one.
finder = pickle.load(f)

sia = SentimentIntensityAnalyzer()


app = Flask(__name__)

target_user = path.join(getcwd(), f"model_data/target_users/") # root target user folder
suffix = "_clean.csv"

analysis_folder = path.join(getcwd(), f"model_data/analysis_folder/") # root analysis folder


twitter_analysis = path.join(analysis_folder, "twitter/")

def perform_analysis(dataframe, profile_id, root_folder):

    img_file = root_folder+profile_id+"_analysis.pdf"
    if path.exists(img_file):
        # analysis already performed.
        # simply return
        print("Analysis file already exists..")
        return 

    print(f"Analysis Job is created for {profile_id}")
    neg_counts = [0,0,0,0,0] # 0:bjp,1:congress, 2:hindu, 3:islam, 4:sikh,5:Others
    pos_counts = [0,0,0,0,0]

    totals = [0,0,0,0,0]


    for tweet in dataframe:
        cat = finder.predict(tweet)
        if cat["bjp"]:
            p = sia.polarity_scores(tweet)
            if p["neg"] > 0.1 and p["pos"]  < 0.1:
                neg_counts[0] += 1
            if p["pos"] > 0.1 and p["neg"]  < 0.1:
                pos_counts[0] += 1
            
            totals[0] += 1
                                
                    
        elif cat["congress"]:
                p = sia.polarity_scores(tweet)
                if p["neg"] > 0.1 and p["pos"]  < 0.1:
                    neg_counts[1] += 1
                if p["pos"] > 0.1 and p["neg"]  < 0.1:
                    pos_counts[1] += 1
                
                totals[1] += 1
                
        elif cat["hindu"]:
            p = sia.polarity_scores(tweet)
            if p["neg"] > 0.1 and p["pos"]  < 0.1:
                neg_counts[2] += 1
            if p["pos"] > 0.1 and p["neg"]  < 0.1:
                pos_counts[2] += 1
                
            totals[2] += 1
                
        elif cat["islam"]:
            p = sia.polarity_scores(tweet)
            if p["neg"] > 0.1 and p["pos"]  < 0.1:
                neg_counts[3] += 1
            if p["pos"] > 0.1 and p["neg"]  < 0.1:
                pos_counts[3] += 1
                
            totals[3] += 1
                
                
        elif cat["sikh"]:
            p = sia.polarity_scores(tweet)
            if p["neg"] > 0.1 and p["pos"]  < 0.1:
                neg_counts[4] += 1
            if p["pos"] > 0.1 and p["neg"]  < 0.1:
                pos_counts[4] += 1
            totals[4] += 1
        # else:
        #     p = sia.polarity_scores(tweet)
        #     if p["neg"] > 0.1 and p["pos"]  < 0.1:
        #         neg_counts[5] += 1
        #     if p["pos"] > 0.1 and p["neg"]  < 0.1:
        #         pos_counts[5] += 1
        #     totals[5] += 1
            
    print(neg_counts, pos_counts, totals)
    keys = ["B", "C", "H", "M", "S"]
    figure, axis = plt.subplots(3,1, constrained_layout=True)

    figure.set_figwidth(15)
    figure.set_figheight(8)

    axis[0].bar(keys, pos_counts, color ='green',
            width = 0.2)
    axis[0].set_title("Positive Content")


    axis[1].bar(keys, neg_counts, color ='red',
            width = 0.2)
    axis[1].set_title("Negative Content")


    axis[2].bar(keys, totals, color ='skyblue',
            width = 0.2)

    axis[2].set_title("Total Content")

    lock.acquire()
    plt.savefig(img_file)
    lock.release()

def execute_twitter_task(profile_id):
    p_file = target_user+"/twitter/"+f"{profile_id}.csv"
    if path.exists(p_file):
        print("User's tweet already scraped.")
        prof = TwitterProfile(profile_id)
        prof.get()
        pth = prof.save_clean()
        dataframe = prof.df()
        tweets = dataframe["tweet"].values # analyzing 100 tweets only for testing purpose only
        Thread(target=perform_analysis, args=(tweets, profile_id, twitter_analysis,)).run()
        return

    print(f"Scraping job is created for {profile_id}")
    prof = TwitterProfile(profile_id)
    prof.get()
    pth = prof.save_clean()
    dataframe = prof.df()

    tweets = dataframe["tweet"].values # analyzing 100 tweets only for testing purpose only

    Thread(target=perform_analysis, args=(tweets, profile_id, twitter_analysis,)).run()

    return pth



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit_job", methods=["POST", "GET"])
def submit_job():
    if request.method == "GET":
        return redirect(url_for("home"))

    if request.method == "POST":
        logging.log(1, request.form)
        plat = request.form.get("platform")
        prof_id = request.form.get("profile_id")
        if plat == "twitter":
            print(plat, prof_id)
            Thread(target=execute_twitter_task, args=(request.form.get("profile_id"), )).start()
        else:
            return render_template("index.html", flag="Platform not yet included for analysis")
       

        return render_template("index.html", flag="Your response was noted and a job was scheduled")


@app.route("/analysis", methods=["POST","GET"])
def analysis():
    if request.method == "GET":
        return render_template("analysis.html")
    if request.method == "POST":
        # extracting profile id and platform from request body
        profile_id = request.form.get("profile_id")
        platform = request.form.get("platform")

        profile_analysis = analysis_folder+f"{platform}/"+f"{profile_id}_analysis.pdf"
        if path.exists(profile_analysis):
            return send_file(profile_analysis, attachment_filename=f"{profile_id}_analysis.pdf")
        else:
            return render_template("analysis.html", flag=f"{profile_id}'s data is not scraped")
        
        return render_template("analysis.html", flag=f"{profile_id} is under analysis")
 


if __name__ == "__main__":
    app.run(debug=True)