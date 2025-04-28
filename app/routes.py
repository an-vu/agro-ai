# -*- coding:utf-8 -*-
"""@package web
This method is responsible for the inner workings of the different web pages in this application.
"""
from flask import render_template, url_for, session, redirect, request
from app import app
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
from app.HeatmapGenerator import showHeatmap
from app import DataPreprocessor, ModelCreator, AppConfig, logic
import os, random

class LabelForm(FlaskForm):
    choice = RadioField(u'Label', choices=[('H', u'Healthy'), ('B', u'Unhealthy')], validators = [DataRequired(message='Cannot be empty')])
    submit = SubmitField('Add Label')

@app.route("/", methods=['GET'])
@app.route("/index.html",methods=['GET'])
def home():
    """
    Operates the root (/) and index(index.html) web pages.
    """
    session.pop('imgQueue', None)
    session.pop('input', None)
    return render_template('index.html')

@app.route('/heatmap')
def heatmap():
    filename = showHeatmap()
    return render_template('heatmap.html', heatmap_img=filename)

@app.route("/label.html",methods=['GET', 'POST'])
def label():
    """
    Operates the label(label.html) web page.
    """

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


@app.route("/intermediate.html",methods=['GET'])
def intermediate():
    """
    Operates the intermediate(intermediate.html) web page.
    """

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
    
    return render_template('feedback.html', healthy_list = h_feedback_result, unhealthy_list = u_feedback_result, healthy_conf_list = h_conf_result, unhealthy_conf_list = u_conf_result, h_list_length = h_length, u_list_length = u_length)

#app.run( host='127.0.0.1', port=5000, debug='True', use_reloader = False)
