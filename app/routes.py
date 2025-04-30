# -*- coding:utf-8 -*-
"""@package web
This method is responsible for the inner workings of the different web pages in this application.
"""
from flask import render_template, session, redirect, url_for
from app import app, HeatmapGenerator
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
from sklearn.model_selection import train_test_split
from PIL import Image
import os, pandas as pd, numpy as np, time, keras, tensorflow as tf

class LabelForm(FlaskForm):
    choice = RadioField(u'Label', choices=[(0, u'Healthy'), (1, u'Unhealthy')], validators = [DataRequired(message='Cannot be empty')])
    submit = SubmitField('Add Label')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'app_cache', 'model.weights.h5')
tf.config.run_functions_eagerly(True)

@app.route("/", methods=['GET'])
@app.route("/index.html",methods=['GET'])
def home():
    """
    Operates the root (/) and index(index.html) web pages.
    """
    # wipe cookies
    session.clear()

    # step 1 - preprocess csv, get labels, randomize data
    path = os.path.join(os.path.dirname(__file__), 'static', 'imgAnnotations.csv')
    df = pd.read_csv(path, index_col=0)
    images = []
    labels = []
    prev = None

    for index, row in df.iterrows():        
        if index == prev:
            continue
        prev = index
        images.append(index)
        if all(row.iloc[:4] == 0):
            labels.append(0)
        else:
            labels.append(1)

    session['x_train'], session['x_test'], session['y_train'], session['y_test'] = train_test_split(images, labels, test_size=0.1, random_state=int(time.time()))

    # step 2 - create model, compile model, save bare model to app_cache
    inputLayer = keras.Input(shape=(256, 256, 3))
    x = keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputLayer)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.MaxPooling2D((2, 2))(x)
    x = keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same', name="attention_layer")(x)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dense(128, activation='relu')(x)
    x = keras.layers.Dropout(0.5)(x)
    output = keras.layers.Dense(1, activation='sigmoid')(x)

    model = keras.Model(inputs=inputLayer, outputs=output)
    model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
    model.save(MODEL_PATH)

    return render_template('index.html')

@app.route('/heatmap')
def heatmap():
    filename = HeatmapGenerator.showHeatmap()
    return render_template('heatmap.html', heatmap_img=filename)

@app.route("/label.html", methods=['GET', 'POST'])
def label():
    """
    Operates the label(label.html) web page.
    Initializes session data if needed and handles labeling logic.
    """
    # step 1 - verify user properly initialized app (thru home)
    if 'x_train' not in session or 'y_train' not in session:
        return redirect(url_for('home'))

    form = LabelForm()

    # step 2 - clear cookies necessary for labeling
    if 'form_images' not in session or 'form_labels' not in session:
        print('new images made, variables set')
        session['form_images'] = session['x_train'][-10:]
        session['form_labels'] = session['y_train'][-10:]
        session['x_train'] = session['x_train'][:-10]
        session['y_train'] = session['y_train'][:-10]
        session['user_x'] = None
        session['user_y'] = None
        session['counter'] = 0

    # step 3 - collect user inputs through form handling
    if form.validate_on_submit():
        # store user's label for current image
        curr_idx = session['counter']
        session['form_labels'][curr_idx] = (form.choice.data)
        session['counter'] += 1

        # after 10 labels, clear cookies, store inputs in user_x and user_y
        if session['counter'] >= len(session['form_images']):
            session['user_x'] = (session.pop('form_images', None))
            session['user_y'] = (session.pop('form_labels', None))
            session.pop('counter', None)

            return redirect(url_for('intermediate'))

        return redirect(url_for('label'))

    # update counter and current image for display
    curr_idx = session['counter']
    curr_img = session['form_images'][curr_idx]
    img_path = url_for('static', filename=f'imgHandheld/{curr_img}')

    return render_template('label.html', form=form, img_path=img_path, curr_idx=curr_idx+1)

@app.route("/intermediate.html",methods=['GET'])
def intermediate():
    """
    Operates the intermediate(intermediate.html) web page.
    """
    # step 1 - preprocess data
    imgNames = session['user_x']
    imgLabels = session['user_y']
    imgMaps = []
    
    for imgName in session['user_x']:
        imgPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', imgName)

        # Open image, convert to RGB, resize to 256x256
        img = Image.open(imgPath).convert('RGB').resize((256, 256))

        # Convert to NumPy array and normalize (0-255 -> 0-1)
        imgArr = np.array(img, dtype=np.float32) / 255.0
        imgMaps.append(imgArr)

    # step 2 - load, compile, and feed model
    model = keras.models.load_model(MODEL_PATH)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    x_user = np.array(imgMaps)
    y_user = np.array(imgLabels).astype(np.float32)
    model.fit(x_user, y_user, epochs=5, batch_size=4, verbose=2)

    loss, accuracy = (f'{x:.2f}' for x in model.evaluate(x_user, y_user, verbose=2))

    model.save(MODEL_PATH)

    # step 3 - sort user inputs to display on intermediate
    userInput = list(zip(session['user_x'], session['user_y']))
    imgH = []
    imgU = []

    for img, label in userInput:
        if label in '0':
            imgH.append(url_for('static', filename=f'imgHandheld/{img}'))
        elif label in '1':
            imgU.append(url_for('static', filename=f'imgHandheld/{img}'))

    return render_template('intermediate.html', accuracy=accuracy, loss=loss, userH=imgH, lenH=len(imgH), userU=imgU, lenU=len(imgU))

@app.route("/final.html", methods=["GET"])
def final():

    training_size = min(len(session['x_train']), 500)


    return render_template('final.html', confidence=0, health_user=0, blight_user=0, healthNum_user=0, blightNum_user=0, health_test=0, unhealth_test=0, healthyNum=0, unhealthyNum=0, healthyPct=0, unhealthyPct=0, h_prob=0, b_prob=0)

#app.run( host='127.0.0.1', port=5000, debug='True', use_reloader = False)
