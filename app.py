from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulating a database with a dictionary, including a role for each user
# Note: Changed 'sha256' to 'pbkdf2:sha256' in generate_password_hash method
users = {
    'admin1@trincoll.edu': {'password': generate_password_hash('415', method='pbkdf2:sha256'), 'role': 'admin'},
    'volunteer1@trincoll.edu': {'password': generate_password_hash('415', method='pbkdf2:sha256'), 'role': 'volunteer'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['login-email']
    password = request.form['login-password']
    user = users.get(email)
    
    if user and check_password_hash(user['password'], password):
        # Login successful
        flash('Login successful!', 'success')
        if user['role'] == 'admin':
            return redirect(url_for('admin_ui'))
        elif user['role'] == 'volunteer':
            return redirect(url_for('volunteer_ui'))
    else:
        # Login failed
        flash('Invalid email or password.', 'danger')
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['signup-email']
    password = request.form['signup-password']
    confirm_password = request.form['signup-confirm-password']

    if email in users:
        flash('Email already exists.', 'danger')
        return redirect(url_for('index'))

    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    users[email] = {'password': hashed_password, 'role': 'volunteer'}  # Default role is volunteer
    flash('Account created successfully, please login.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_ui():
    # Ensure this page has some form of access control in a real application
    return render_template('admin_ui.html')

@app.route('/volunteer')
def volunteer_ui():
    # Ensure this page has some form of access control in a real application
    return render_template('volunteer_ui.html')





#Volunteer stuffs WIP
import sqlite3

def connect_db():
    return sqlite3.connect('volunteer_hours.db')

# Route for the volunteer interface to log hours
@app.route('/log_hours', methods=['GET', 'POST'])
def log_hours():
    if request.method == 'POST':
        volunteer_name = request.form['volunteer_name']
        shift_id = request.form['shift_id']
        hours_worked = request.form['hours_worked']
        # Insert the logged hours into the database
        db = connect_db()
        cur = db.cursor()
        cur.execute('INSERT INTO hours (volunteer_name, shift_id, hours_worked) VALUES (?, ?, ?)',
                    (volunteer_name, shift_id, hours_worked))
        db.commit()
        db.close()
        flash('Hours logged successfully', 'success')
        return redirect(url_for('log_hours'))
    else:
        # Fetch shift data from the database and pass it to the template
        db = connect_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM shifts')
        shifts = cur.fetchall()
        db.close()
        return render_template('log_hours.html', shifts=shifts)

# Route for the administrator interface to manage hours
@app.route('/manage_hours')
def manage_hours():
    db = connect_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM hours')
    logged_hours = cur.fetchall()
    db.close()
    return render_template('manage_hours.html', logged_hours=logged_hours)

#End of Volunteer stuffs


#GoogleCalendar API- Hamim- 04.07.2024
import os
from flask import Flask, redirect, url_for, session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests


#app = Flask(__name__)
#app.secret_key = 'your_secret_key'

# Load client secrets
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Required only for development
GOOGLE_CLIENT_ID = "208062345148-mp5pboco1qgjcfveer33s5748tm5qnlm.apps.googleusercontent.com"
client_secrets_file = os.path.join(os.path.dirname(__file__), "google_oauth_config.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/calendar"],
    redirect_uri="http://localhost:5003/oauth2callback"
)

@app.route('/login/oauth2callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not flow.credentials.is_valid():
        return 'Failed to fetch valid credentials', 401

    # Save credentials in the session or database as needed
    session['credentials'] = {
        'token': flow.credentials.token,
        'refresh_token': flow.credentials.refresh_token,
        'token_uri': flow.credentials.token_uri,
        'client_id': flow.credentials.client_id,
        'client_secret': flow.credentials.client_secret,
        'scopes': flow.credentials.scopes,
    }

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
