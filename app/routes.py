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

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'static', 'model.weights.h5')
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
    model.compile(loss='binary_crossentropy', optimizer='SGD', metrics=['accuracy'])
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
<<<<<<< HEAD

    form = LabelForm()

    if 'input' not in session:
        session['input'] = {}

    if 'imgQueue' not in session or not session['imgQueue']:
        if len(session['input']) >= 10:
            return redirect(url_for('intermediate'))
        else:
            session['imgQueue'] = logic.fetchImg(10, session['input'])
            session.modified = True

    if form.validate_on_submit():
        current_img = session['imgQueue'].pop(0)
        session['input'][current_img] = form.choice.data
        session.modified = True

        if not session['imgQueue']:
            print(session['input'])
            return redirect(url_for('intermediate'))

        return redirect(url_for('label'))

    current_img = session['imgQueue'][0]
    return render_template('label.html', form=form, image_path=current_img)
=======
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
        if 'user_x' not in session or 'user_y' not in session:
            session['user_x'] = []
            session['user_y'] = []
        session['counter'] = 0
>>>>>>> master

    # step 3 - collect user inputs through form handling
    if form.validate_on_submit():
        # store user's label for current image
        curr_idx = session['counter']
        session['form_labels'][curr_idx] = (form.choice.data)
        session['counter'] += 1

        # after 10 labels, clear cookies, store inputs in user_x and user_y
        if session['counter'] >= len(session['form_images']):
            session['user_x'] += (session.pop('form_images', None))
            session['user_y'] += (session.pop('form_labels', None))
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
<<<<<<< HEAD

    session['imgQueue'] = logic.fetchImg(10, session['input'])

    unhealthy_images = [img for img, label in session['input'].items() if label == 'B']
    healthy_images = [img for img, label in session['input'].items() if label == 'H']

    return render_template(
        'intermediate.html',
        health_user=healthy_images,
        blight_user=unhealthy_images,
        healthNum_user=len(healthy_images),
        blightNum_user=len(unhealthy_images),
    )

'''
@app.route("/final.html",methods=['GET'])
def final():
    """
    Operates the final(final.html) web page.
    """
    healthyList = []
    blightedList = []
    for key in session['input']:
        if session['input'][key] == 'H':
            healthyList.append(key)
        else:
            blightedList.append(key)



    return render_template('final.html')
'''

@app.route("/final.html", methods=["GET"])
def final():
    labeled_images = session.get('labeled_images', [])
    labels = session.get('labels', [])

    if not labeled_images or not labels:
        return redirect(url_for('home'))

    # Split healthy and unhealthy images
    health_user = [img for img, lbl in zip(labeled_images, labels) if lbl == 'H']
    blight_user = [img for img, lbl in zip(labeled_images, labels) if lbl == 'B']

    healthNum_user = len(health_user)
    blightNum_user = len(blight_user)

    # Dummy variables for machine results (these would normally be AI outputs)
    health_test = []
    unhealth_test = []
    healthyNum = 0
    unhealthyNum = 0
    healthyPct = "0%"
    unhealthyPct = "0%"
    h_prob = []
    b_prob = []

    # Dummy confidence value (adjust later)
    confidence = 0.85

    return render_template(
        'final.html',
        confidence=confidence,
        health_user=health_user,
        blight_user=blight_user,
        healthNum_user=healthNum_user,
        blightNum_user=blightNum_user,
        health_test=health_test,
        unhealth_test=unhealth_test,
        healthyNum=healthyNum,
        unhealthyNum=unhealthyNum,
        healthyPct=healthyPct,
        unhealthyPct=unhealthyPct,
        h_prob=h_prob,
        b_prob=b_prob
    )


@app.route("/feedback/<h_list>/<u_list>/<h_conf_list>/<u_conf_list>",methods=['GET'])
def feedback(h_list,u_list,h_conf_list,u_conf_list):
    """
    Operates the feedback(feedback.html) web page.
    """
    h_feedback_result = list(h_list.split(","))
    u_feedback_result = list(u_list.split(","))
    h_conf_result = list(h_conf_list.split(","))
    u_conf_result = list(u_conf_list.split(","))
    h_length = len(h_feedback_result)
    u_length = len(u_feedback_result)
=======
    # step 1 - preprocess data
    imgNames = session['user_x']
    imgLabels = session['user_y']
    imgMaps = []
>>>>>>> master
    
    for imgName in imgNames:
        imgPath = os.path.join(os.path.dirname(__file__), 'static', 'imgHandheld', imgName)

        # Open image, convert to RGB, resize to 256x256
        img = Image.open(imgPath).convert('RGB').resize((256, 256))

        # Convert to NumPy array and normalize (0-255 -> 0-1)
        imgArr = np.array(img, dtype=np.float32) / 255.0
        imgMaps.append(imgArr)

    # step 2 - load, compile, and feed model
    model = keras.models.load_model(MODEL_PATH)
    model.compile(optimizer='SGD', loss='binary_crossentropy', metrics=['accuracy'])
    x_user = np.array(imgMaps)
    y_user = np.array(imgLabels).astype(np.float32)
    model.fit(x_user, y_user, epochs=5, batch_size=4, verbose=2)

    loss, accuracy = (f'{x*100:.2f}' for x in model.evaluate(x_user, y_user, verbose=2))

    model.save(MODEL_PATH)

    # step 3 - sort user inputs to display on intermediate
    userInput = list(zip(session['user_x'][-10:], session['user_y'][-10:]))
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
    y_test_arr = np.array(y_test).astype(np.float32)

    # Predict probabilities
    probs = model.predict(x_test_arr).flatten()
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
    user_data = list(zip(session['user_x'][-10:], session['user_y'][-10:]))
    userH = [url_for('static', filename=f'imgHandheld/{img}') for img, label in user_data if str(label) == '0']
    userU = [url_for('static', filename=f'imgHandheld/{img}') for img, label in user_data if str(label) == '1']
    lenUH = len(userH)
    lenUU = len(userU)

    # Evaluate to get confidence/accuracy
    _, accuracy = model.evaluate(x_test_arr, y_test_arr, verbose=0)
    confidence = f'{accuracy * 100:.2f}%'

    return render_template(
        'final.html',
        confidence=confidence,
        userH=userH,
        userU=userU,
        lenUH=lenUH,
        lenUU=lenUU,
        modelH=modelH,
        modelU=modelU,
        lenMH=lenMH,
        lenMU=lenMU,
        percentH=percentH,
        percentU=percentU,
        probArrH=probArrH,
        probArrU=probArrU
    )