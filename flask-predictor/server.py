# Create API of ML model using flask
from wtforms.validators import Required
import requests
'''
This code takes the JSON data while POST request an performs the prediction using loaded model and returns
the results in JSON format.
'''
# Import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for
from datetime import datetime
import pickle
import textwrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap



app = Flask(__name__)
# Key que protege "against Cross-Site Request Forgery (CSRF) attacks"
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title='Home Page',year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', title='Acerca', year=datetime.now().year)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Home Page', year=datetime.now().year)


@app.route('/exemplo1')
def exemplo1():
    url = 'http://localhost:5000/api'

    # Criar uma página de exemplo

    # Change the value of experience that you want to test
    r = requests.post(url, json={'exp': 1.8, })
    return 'Oi:<b>'+ str(r.json()) + '</b>'

@app.route('/exemplo2')
def exemplo2():
    url = 'http://localhost:5000/api'
    r = requests.post(url, json={'exp': 1.8, })

    return render_template('resultado.html', title='resultado', message=r.json())

class NameForm(FlaskForm):
    experience = StringField('What is your experience?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/exemplo3', methods=['GET','POST'])
def exemplo3():
    experience = None
    form = NameForm()
    if form.validate_on_submit():
        experience = form.experience.data
        #url = 'http://localhost:5000/api'
        #r = requests.post(url, json={'exp': experience, })
        #flash(r)
        session['experience'] = form.experience.data
        flash('Teste'+experience)
        form.experience.data = ''
        return redirect(url_for('exemplo3'))
    return render_template('resultado.html', form=form, experience=session.get('experience'))

@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    # Load the model
    model = pickle.load(open('model.pkl', 'rb'))
    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict([[np.array(data['exp'])]])
    # Take the first value of prediction
    output = prediction[0]

    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
