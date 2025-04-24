import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from flask import session, render_template, url_for
from io import StringIO
from app.JackPreprocess import process
from app.ModelCreator import createMLModel
import os
import random

# This getData function grabs the images from the S3 bucket
def getData():
    path = 's3://agro-ai-maize/csvOut.csv'

    try:
        data = pd.read_csv(path, index_col=0, header=None)
        fileLabels = data.loc[:, [data.columns[0], data.columns[-1]]]
        imgDict = dict(zip(data.index, data.iloc[:, -1]))
    except FileNotFoundError:
        print('Error: ' + path + ' not found.')

    URLs = process.getURL(imgDict)
    return imgDict, URLs


def fetchImg(n, seen):
    cnt = 0
    image_folder = 'app/static/imgHandheld/'
    image_files = os.listdir(image_folder)
    seenImgs = list(seen.keys())
    image_paths = []

    while len(image_paths) < n:
        selected_image = random.choice(image_files)
        if selected_image not in seenImgs and cnt < 40:
            image_paths.append(f'static/imgHandheld/{selected_image}')
        cnt += 1

    return image_paths