import numpy as np
from flask import Flask, redirect, render_template, request, session

from data_model import make_prediction, display_probability

app = Flask(__name__, static_folder="static")
app.secret_key = 'secret'
# user login credentials
user = {"username": "test", "password": "test"}


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return redirect('/home')

        return redirect("/invalid")  # If the username or password does not matches

    return render_template("log_in.html")


@app.route('/invalid', methods=['POST', 'GET'])
def invalid():
    if 'user' in session and session['user'] == user['username']:
        return render_template("invalid.html")
    if request.method == 'GET':
        return redirect('/')


@app.route('/home', methods=['POST', 'GET'])
def home():
    if 'user' in session and session['user'] == user['username']:
        return render_template("home.html")

    return '<h1>You are not logged in.</h1>'


@app.route('/prediction', methods=['POST', 'GET'])
def result():
    gender = int(request.form['gender'])
    age = int(request.form['age'])
    ht = int(request.form['hypertension'])
    hd = int(request.form['heart_disease'])
    married = int(request.form['ever_married'])
    work = int(request.form['work_type'])
    residence = int(request.form['Residence_type'])
    glucose = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    smoke = int(request.form['smoking_status'])

    info = np.array([gender, age, ht, hd, married, work, residence, glucose, bmi, smoke]).reshape(1, -1)

    prediction = make_prediction(info)
    if prediction == 0:
        risk = 'LOW'
        title = 'LOW'
    else:
        risk = 'HIGH'
        title = 'HIGH'

    probability = display_probability(info)

    return render_template('prediction.html', title=title, risk=risk, prob=round(probability,2))


if __name__ == "__main__":
    app.run(debug=True)