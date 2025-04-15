import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from flask import session, render_template, url_for
from io import StringIO
from app.JackPreprocess import process
from app.ModelCreator import createMLModel

# This getData function grabs the images from the S3 bucket
def getData():
    path = 's3://agro-ai-maize/csvOut.csv'

    try:
        data = pd.read_csv(path, index_col=0, header=None)
        fileLabels = data.loc[:, [data.columns[0], data.columns[-1]]]
        imgDict = dict(zip(data.index, data.iloc[:, -1]))
        print(f'\nIMGDICT:\n{imgDict}')
    except FileNotFoundError:
        print('Error: ' + path + ' not found.')

    URLs = process.getURL(imgDict)
    return imgDict, URLs


def getNextSetOfImages():
    data, URLs = getData()
    ml_model = createMLModel(data)

    # This might be useful, I was thinking of doing something like this to grab the images
    #test_set = data[data.index.isin(train_img_names) == False]

    #test_set = []
    #for i in range(2):
        #test_set.append(data)3
