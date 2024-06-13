# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Define countries and their respective factors
countries = {
    "France": 1.8,
    "Germany": 1.7,
    "Spain": 1.6,
    "Italy": 1.5,
    "Portugal": 1.4
}

# Default password
default_password = "Epwd123"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if password == default_password:
            return redirect(url_for('index', name=name))
    return render_template('login.html')

@app.route('/index')
def index():
    name = request.args.get('name')
    return render_template('index.html', name=name, countries=countries)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    country = request.form['country']
    amount = float(request.form['amount'])
    factor = countries[country]
    result = amount * factor

    with open('data/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, country, amount, factor, result])

    return redirect(url_for('view'))

@app.route('/view')
def view():
    entries = []
    with open('data/output.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            entries.append(row)
    return render_template('view.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
