#this cleans the fittocsv-data converted file when there are duplicate entries

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
  

DEBUG = True
SHOW = True
SAVE = not SHOW

def log(s):
    if DEBUG:
        print(s)

root = os.path.dirname(os.path.realpath(__file__)) # This gets the current local path
root = root + '\\'
log(root)

full_root = []
datafiles = []
filename = []
df_name = []

for file in os.listdir(root): #Finds the data.csv
    if file.endswith("data.csv"): # Don't change this, I want the _data.csv files
        filename.append(file)
        full_root.append(root + file)
        log(full_root)

#This reads all the csv files via Pandas data interperted into a pandas data frame
log("File will be cleaned. If problems press ctrl-c to kill python from the terminal")
if (len(filename) == 1) :
    df=pd.read_csv(full_root[0])
    df.drop_duplicates(subset='record.timestamp[s]',keep='first',inplace=True)
    df.set_index('record.timestamp[s]', inplace=True, drop=True)
    new_index = pd.Index(np.arange(df.index.min(),df.index.max(),1), name="record.timestamp_x[s]")
    df = df.reindex(new_index)
    df = df.interpolate()
    df.to_csv(root + filename[0] + "-clean.csv", sep=',')
else:
    print("Too many files with data.csv ending")
