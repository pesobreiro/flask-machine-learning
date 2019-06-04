# Create API of ML model using flask

'''
This code takes the JSON data while POST request an performs the prediction using loaded model and returns
the results in JSON format.
'''

# Import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pickle
import textwrap

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl','rb'))
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


@app.route("/teste")
def teste():
    return "12"
    """
    <html>
    <header><title>Teste</title></header>
    <body>
        teste
    </body>
    <br>
    </html>
    """


@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict([[np.array(data['exp'])]])

    # Take the first value of prediction
    output = prediction[0]

    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
