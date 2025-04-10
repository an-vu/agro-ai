import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from flask import session, render_template, url_for
from io import StringIO
from app.JackPreprocess import process
#from app.ModelCreator import ML_Model, Active_ML_Model
#from app.DataPreprocessor import DataPreprocessing

def getData():
    path = 's3://agro-ai-maize/csvOut.csv'
    print(path)

    try:
        data = pd.read_csv(path, index_col=0, header=None)
        fileLabels = data.loc[:, [data.columns[0], data.columns[-1]]]
        imgDict = dict(zip(data.index, data.iloc[:, -1]))
        print(f'\nIMGDICT:\n{imgDict}')
    except FileNotFoundError:
        print('Error: ' + path + ' not found.')

    URLs = process.getURL(imgDict)

def createMLModel(data):
    train_img_names, train_img_label = list(zip(*session['train']))
    train_set = data.loc[train_img_names, :]
    train_set['y_value'] = train_img_label
    ml_model = ML_Model(train_set, RandomForestClassifier(), DataPreprocessing(True))
    return ml_model, train_img_names

def renderLabel(form):
    queue = session['queue']
    img = queue.pop()
    session['queue'] = queue
    return render_template(url_for('label'), form=form, picture=img, confidence=session['confidence'])

def initializeAL(form, confidence_break=0.7):
    preprocess = DataPreprocessing(True)
    ml_classifier = RandomForestClassifier()
    data = getData()
    al_model = Active_ML_Model(data, ml_classifier, preprocess)

    session['confidence'] = 0
    session['confidence_break'] = confidence_break
    session['labels'] = []
    session['sample_idx'] = list(al_model.sample.index.values)
    session['test'] = list(al_model.test.index.values)
    session['train'] = al_model.train
    session['model'] = True
    session['queue'] = list(al_model.sample.index.values)

    return renderLabel(form)

def getNextSetOfImages(form, sampling_method):
    data = getData()
    ml_model, train_img_names = createMLModel(data)
    test_set = data[data.index.isin(train_img_names) == False]

    session['sample_idx'], session['test'] = sampling_method(ml_model, test_set, 5)
    session['queue'] = session['sample_idx'].copy()

    return renderLabel(form)

def prepareResults(form):
    session['labels'].append(form.choice.data)
    session['sample'] = tuple(zip(session['sample_idx'], session['labels']))

    if session['train'] is not None:
        session['train'] += session['sample']
    else:
        session['train'] = session['sample']

    data = getData()
    ml_model, train_img_names = createMLModel(data)

    session['confidence'] = np.mean(ml_model.K_fold())
    session['labels'] = []

    if session['confidence'] < session['confidence_break']:
        health_pic, blight_pic = ml_model.infoForProgress(train_img_names)
        return render_template(
            'intermediate.html',
            form=form,
            confidence="{:.2%}".format(round(session['confidence'], 4)),
            health_user=health_pic,
            blight_user=blight_pic,
            healthNum_user=len(health_pic),
            blightNum_user=len(blight_pic)
        )
    else:
        test_set = data.loc[session['test'], :]
        health_user, blight_user, health, blight, h_prob, b_prob = ml_model.infoForResults(train_img_names, test_set)
        return render_template(
            'final.html',
            form=form,
            confidence="{:.2%}".format(round(session['confidence'], 4)),
            health_user=health_user,
            blight_user=blight_user,
            healthNum_user=len(health_user),
            blightNum_user=len(blight_user),
            health_test=health,
            unhealth_test=blight,
            healthyNum=len(health),
            unhealthyNum=len(blight),
            healthyPct="{:.2%}".format(len(health) / (200 - (len(health_user) + len(blight_user)))),
            unhealthyPct="{:.2%}".format(len(blight) / (200 - (len(health_user) + len(blight_user)))),
            h_prob=h_prob,
            b_prob=b_prob
        )