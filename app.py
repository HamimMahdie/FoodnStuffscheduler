from flask import Flask, render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulating a database with a dictionary, including a role for each user
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
        session['user_email'] = email  # Save the user's email in the session
        flash('Login successful!', 'success')
        if user['role'] == 'admin':
            return redirect(url_for('admin_ui'))
        elif user['role'] == 'volunteer':
            return redirect(url_for('volunteer_ui'))
    else:
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

# Database connection function
def connect_db():
    return sqlite3.connect('volunteer_hours.db')

@app.route('/post_shift', methods=['POST'])
def post_shift():
    title = request.form['shift_title']
    start_datetime = request.form['start_datetime']
    end_datetime = request.form['end_datetime']
    description = request.form['description']

    db = connect_db()
    cur = db.cursor()
    cur.execute('INSERT INTO shifts (title, start_time, end_time, description) VALUES (?, ?, ?, ?)',
                (title, start_datetime, end_datetime, description))
    db.commit()
    db.close()
    flash('Shift posted successfully.', 'success')
    return redirect(url_for('admin_ui'))


@app.route('/admin')
def admin_ui():
    return render_template('admin_ui.html')


@app.route('/volunteer')
def volunteer_ui():
    db = connect_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM shifts')
    shifts = cur.fetchall()
    db.close()
    return render_template('volunteer_ui.html', shifts=shifts)


def init_db():
    db = connect_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT
        )
    ''')
    db.commit()
    db.close()

init_db()

# Database connection function
def connect_db():
    return sqlite3.connect('volunteer_hours.db')

# Route for the volunteer interface to log hours
@app.route('/log_hours', methods=['GET', 'POST'])
def log_hours():
    if request.method == 'POST':
        volunteer_name = request.form['volunteer_name']
        shift_id = request.form['shift_id']
        hours_worked = request.form['hours_worked']
        email = session.get('user_email')  # Retrieve email from session
        db = connect_db()
        cur = db.cursor()
        cur.execute('INSERT INTO hours (volunteer_name, email, shift_id, hours_worked) VALUES (?, ?, ?, ?)',
                    (volunteer_name, email, shift_id, hours_worked))
        db.commit()
        db.close()
        flash('Hours logged successfully', 'success')
        return redirect(url_for('log_hours'))
    else:
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
