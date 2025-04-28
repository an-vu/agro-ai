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
    return render_template('intermediate.html')

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
