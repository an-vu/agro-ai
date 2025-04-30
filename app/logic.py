import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from flask import session, render_template, url_for
from io import StringIO
from app import DataPreprocessor, ModelCreator, AppConfig, JackPreprocess
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

def initModel(): # May need to be updated later for better user interaction
    train_generator, (xTest, yTest) = DataPreprocessor.preprocessData()
    model = ModelCreator.createCNNModel()

    if not AppConfig.RETRAIN_MODEL and os.path.exists(AppConfig.WEIGHT_PATH):
        model.load_weights(AppConfig.WEIGHT_PATH)
    else:
        model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
        model.fit(train_generator, epochs=2, validation_data=(xTest, yTest))
        model.save_weights(AppConfig.WEIGHT_PATH)

    return model
    
def getConfidence(model, img):
    confidence = model.predict(img)[0][0]

    if confidence >= 0.5:
        return (1, confidence)  # Predicts Class 1
    else:
        return (0, 1 - confidence)  # Predicts Class 0
    
def showModelConf(model, n):
    images = fetchImg(10, [])
    confidenceDict = {}

    for img in images:
        confidenceDict[img] = getConfidence(model, img)

    return confidenceDict