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
import os, cv2, pandas as pd, numpy as np, time, keras, tensorflow as tf, matplotlib.pyplot as plt

class LabelForm(FlaskForm):
    choice = RadioField(u'Label', choices=[(0, u'Healthy'), (1, u'Unhealthy')], validators = [DataRequired(message='Cannot be empty')])
    submit = SubmitField('Add Label')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'static', 'model.weights.keras')
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

    # step 2 - create model, compile model, save bare model to static
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
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.save(MODEL_PATH)

    return render_template('index.html')

@app.route('/heatmap')
def heatmap():

    return render_template('heatmap.html', heatmap_img=os.path.join(os.path.dirname(__file__), 'static', 'heatmap_output.png'))

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
        session['form_images'] = session['x_train'][-10:]
        session['form_labels'] = session['y_train'][-10:]
        session['x_train'] = session['x_train'][:-10]
        session['y_train'] = session['y_train'][:-10]
        if 'x_user' not in session or 'y_user' not in session:
            session['x_user'] = []
            session['y_user'] = []
        session['counter'] = 0
    elif len(session['form_images']) <= 0 or len(session['form_labels']) <= 0:
        return redirect(url_for('final'))

    # step 3 - collect user inputs through form handling
    if form.validate_on_submit():
        # store user's label for current image
        curr_idx = session['counter']
        session['form_labels'][curr_idx] = (form.choice.data)
        session['counter'] += 1

        # after 10 labels, clear cookies, store inputs in x_user and y_user
        if session['counter'] >= len(session['form_images']):
            session['x_user'] += (session.pop('form_images', None))
            session['y_user'] += (session.pop('form_labels', None))
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
    x_user = session['x_user']
    y_user = session['y_user']
    x_user_maps = []

    x_test = session['x_test']
    y_test = session['y_test']
    x_test_maps = []
    
    for imgName in x_user:
        imgPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', imgName)

        # Open image, convert to RGB, resize to 256x256
        img = Image.open(imgPath).convert('RGB').resize((256, 256))

        # Convert to NumPy array and normalize (0-255 -> 0-1)
        imgArr = np.array(img, dtype=np.float32) / 255.0
        x_user_maps.append(imgArr)

    x_user = np.array(x_user_maps)
    y_user = np.array(y_user).astype(np.float32).reshape(-1, 1)

    for imgName in x_test:
        imgPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', imgName)

        # Open image, convert to RGB, resize to 256x256
        img = Image.open(imgPath).convert('RGB').resize((256, 256))

        # Convert to NumPy array and normalize (0-255 -> 0-1)
        imgArr = np.array(img, dtype=np.float32) / 255.0
        x_test_maps.append(imgArr)

    test_x = np.array(x_test_maps)
    test_y = np.array(y_test).astype(np.int32).reshape(-1, 1)

    # step 2 - load, compile, and feed model
    model = keras.models.load_model(MODEL_PATH)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    model.fit(x_user, y_user, epochs=1, batch_size=len(x_user), verbose=1)

    loss, accuracy = model.evaluate(test_x, test_y, verbose=0)
    loss = f'{loss * 100:.2f}'
    accuracy = f'{accuracy * 100:.2f}'

    model.save(MODEL_PATH)

    # step 3 - sort user inputs to display on intermediate
    userInput = list(zip(session['x_user'][-10:], session['y_user'][-10:]))
    userH, userU = [], []

    for img, label in userInput:
        if label in '0':
            userH.append(url_for('static', filename=f'imgHandheld/{img}'))
        elif label in '1':
            userU.append(url_for('static', filename=f'imgHandheld/{img}'))

    return render_template('intermediate.html', accuracy=accuracy, loss=loss, userH=userH, lenH=len(userH), userU=userU, lenU=len(userU))

@app.route("/final.html", methods=["GET"])
def final():
    # Load model
    model = keras.models.load_model(MODEL_PATH)
    
    # Load remaining training image names and labels
    x_train = session['x_train']
    y_train = session['y_train']


    # Load test image names and labels
    x_test = session['x_test']
    y_test = session['y_test']

    test_imgs = []
    for imgName in x_test:
        imgPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', imgName)
        img = Image.open(imgPath).convert('RGB').resize((256, 256))
        imgArr = np.array(img, dtype=np.float32) / 255.0
        test_imgs.append(imgArr)

    x_test_arr = np.array(test_imgs)
    y_test_arr = np.array(y_test).astype(np.int32).reshape(-1, 1)

    # Predict probabilities
    probs = model.predict(x_test_arr)
    print(probs)
    probs = probs.flatten()
    preds = (probs > 0.5).astype(int)

    # Separate image URLs and confidence per predicted label
    modelH, modelU = [], []
    probArrH, probArrU = [], []

    for img_name, pred, prob in zip(x_test, preds, probs):
        print(pred, prob)
        if pred == 0:
            modelH.append(url_for('static', filename=f'imgHandheld/{img_name}'))
            probArrH.append(f'{(1 - prob) * 100:.2f}%')
        else:
            modelU.append(url_for('static', filename=f'imgHandheld/{img_name}'))
            probArrU.append(f'{prob * 100:.2f}%')

    # Calculate percentages
    total = len(x_test)
    lenMH = len(modelH)
    lenMU = len(modelU)
    percentH = f'{(lenMH / total) * 100:.2f}%' if total else '0%'
    percentU = f'{(lenMU / total) * 100:.2f}%' if total else '0%'

    # Pull user-labeled data
    user_data = list(zip(session['x_user'][-10:], session['y_user'][-10:]))
    userH = [url_for('static', filename=f'imgHandheld/{img}') for img, label in user_data if str(label) == '0']
    userU = [url_for('static', filename=f'imgHandheld/{img}') for img, label in user_data if str(label) == '1']
    lenUH = len(userH)
    lenUU = len(userU)

    # Evaluate to get confidence/accuracy
    loss, accuracy = model.evaluate(x_test_arr, y_test_arr, verbose=0)
    confidence = f'{accuracy * 100:.2f}%'

    return render_template('final.html', confidence=confidence, userH=userH, userU=userU, lenUH=lenUH,
                           lenUU=lenUU, modelH=modelH, modelU=modelU, lenMH=lenMH, lenMU=lenMU,
                           percentH=percentH, percentU=percentU, probArrH=probArrH, probArrU=probArrU)