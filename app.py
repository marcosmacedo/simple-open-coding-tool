from flask import Flask, render_template, request, redirect, flash
import pandas as pd
from datetime import datetime
from dateutil import tz

app = Flask(__name__)
app.secret_key = b'a secret key'

#Some Global Variables (bad pratice to use them)
df = None
remaining_df = None
current_count = 0
start_time = None
current_entry = None
alert_title = None
alert_desc = None
bot_first = None
current_url = None
is_done = False
current_index = None
current_labels = None

#Settings for the tool. Replace with the dataset path
dataset_path = "samples/to_label_keywords_allyears.csv"

def load_dataset():
    global df
    global remaining_df

    df = pd.read_csv(dataset_path)

    if "index" not in df.columns:
        df["index"] = range(0, df.shape[0])

    #Remove entries that were validated previously
    if "_meta_validated" in df.columns:
        previously_validated = df[df["_meta_validated"] == True]
        current_count = previously_validated.shape[0]
        remaining_df = df[df["_meta_validated"] == False].reset_index(drop=True)
    else:
        df["_meta_validated"] = False

        if "label" not in df.columns:
            df["label"] = ""
        if "comment" not in df.columns:
            df["comment"] = ""
        remaining_df = df.copy()

def get_next_entry():
    global alert_title
    global alert_desc
    global bot_first
    global remaining_df
    global current_url
    global pre_url
    global current_entry
    global is_done
    global current_index
    global current_labels

    #Reload everything
    load_dataset()

    #Load the next entry
    if remaining_df.shape[0] > 0:
        current_entry = remaining_df.iloc[0]
        remaining_df = remaining_df.drop(index=0).reset_index(drop=True)
        alert_title = "Browsing URL"
        alert_desc = current_entry.url
        current_url = current_entry.url
        current_index = current_entry["index"]
        current_labels = df["label"].dropna().unique()
    else:
            alert_title = "All done!"
            alert_desc = "Good job" 
            current_url = "https://google.com"
            is_done = True 

#Initial setup
load_dataset()
get_next_entry()

@app.route("/")
def main():
    return render_template('index.html', 
    df_size=remaining_df.shape[0]+1,
    alert_title=alert_title,
    alert_desc=alert_desc,
    current_count=current_count,
    iframe_url=current_url,
    index=current_index,
    current_labels=current_labels)

@app.route("/process", methods=['POST'])
def process_entry():
    global current_count
    
    if not is_done:
        index = request.form["index"]
        index_in_df = df[df["index"] == int(index)].index[0]
        df.at[index_in_df, "_meta_validated"] = True
        df.at[index_in_df, "comment"] = request.form["comment"] if "comment" in request.form else ""

        label = None

        if request.form["new_label"] == "":
            if request.form["existing_label"] != "-1":
                label = request.form["existing_label"]
            else:
                #Must choose something
                flash('You need to choose an existing label or write a new one', 'error')
                return redirect("/", code=302) 
        else:
            if request.form["existing_label"] == "-1":
                label = request.form["new_label"]
            else:
                #Must choose empty existing label
                flash('You chose an existing label but also created a new one', 'error')
                return redirect("/", code=302) 
            

        df.at[index_in_df, "label"] = label
        current_count = current_count + 1
        
        #Save to disk
        df.to_csv(dataset_path, index=False)

        get_next_entry()

    return redirect("/", code=302)