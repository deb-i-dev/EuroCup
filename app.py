from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# Define predefined users
predefined_users = {
    "user1": User(id=1, username="user1", password=generate_password_hash("password1")),
    "Deb_i": User(id=2, username="Deb_i", password=generate_password_hash("Debipwd")),
    "Abhijeet": User(id=3, username="Abhijeet", password=generate_password_hash("Abhipass3")),
    "Ani": User(id=4, username="Ani", password=generate_password_hash("Aniword4")),
    "Ankur": User(id=16, username="Ankur", password=generate_password_hash("Ankurpwd16")),
    "Ashly": User(id=5, username="Ashly", password=generate_password_hash("Ashlypd5")),
    "Dhiren": User(id=6, username="Dhiren", password=generate_password_hash("DhirenPWD6")),
    "Jainendra": User(id=7, username="Jainendra", password=generate_password_hash("JaiPWD7")),
    "Nilesh": User(id=8, username="Nilesh", password=generate_password_hash("Nileshpwd8")),
    "Prateek": User(id=9, username="Prateek", password=generate_password_hash("PrateekPwd9")),
    "Shivaram": User(id=10, username="Shivaram", password=generate_password_hash("Shivarampd10")),
    "Simant": User(id=11, username="Simant", password=generate_password_hash("Simantpw11")),
    "Sravan": User(id=12, username="Sravan", password=generate_password_hash("Sravanpwd12")),
    "Suprabhat": User(id=13, username="Suprabhat", password=generate_password_hash("Suprabhatwd13")),
    "Supratim": User(id=14, username="Supratim", password=generate_password_hash("Supratimpd14")),
    "Test11": User(id=15, username="Test11", password=generate_password_hash("password15")),
}

# Convert predefined_users to users dictionary
users = {
    user.username: user for user in predefined_users.values()
}


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    countries = {
        "Netherlands": 1.15,
        "Poland": 4.5,
        "Draw": 3.5,
    }
    return render_template('index.html', name=current_user.username, countries=countries)


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    name = request.form['name']
    country = request.form['country']
    amount = request.form['amount']
    factor = request.form['factor']
    result = float(amount) * float(factor)

    # Round the result to 2 decimal places
    rounded_result = round(result, 2)

    # Save the submission to a CSV file
    with open('submissions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, country, amount, factor, rounded_result])

    flash('Your submission has been recorded!')
    return redirect(url_for('index'))


@app.route('/view')
@login_required
def view():
    entries = []
    try:
        with open('submissions.csv', newline='') as file:
            reader = csv.reader(file)
            entries = list(reader)
    except FileNotFoundError:
        pass
    return render_template('view.html', entries=entries)


@app.route('/schedule')
@login_required
def schedule():
    # Hardcoded schedule for demonstration
    schedule_data = [
        {"date": "2024-06-16", "team1": "Netherlands", "team2": "Poland"},
        {"date": "2024-06-16", "team1": "Slovenia", "team2": "Denmark"},
        {"date": "2024-06-17", "team1": "Serbia", "team2": "England"},
        {"date": "2024-06-17", "team1": "Romania", "team2": "Ukraine"},
        {"date": "2024-06-17", "team1": "Belgium", "team2": "Slovakia"},
        # Add more matches here
    ]
    return render_template('schedule.html', schedule_data=schedule_data)


if __name__ == '__main__':
    app.run(debug=True)
