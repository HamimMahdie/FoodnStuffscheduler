from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import Flask
from email_service import init_mail

from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulating a database with a dictionary, including a role for each user
users = {
    'admin1@trincoll.edu': {'password': generate_password_hash('415', method='pbkdf2:sha256'), 'role': 'admin'},
    'volunteer1@trincoll.edu': {'password': generate_password_hash('415', method='pbkdf2:sha256'), 'role': 'volunteer'}
}


# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '[YOU HAVE TO ENTER EMAIL HERE]'
app.config['MAIL_PASSWORD'] = '[YOU HAVE TO ENTER APP PASSWORDS HERE]'

init_mail(app)  # Initialize the mail configuration from email_service


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['login-email']
        password = request.form['login-password']
        role_requested = request.form['role']  # Retrieve the role from the form
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['user_email'] = email  # Save the user's email in the session
            if role_requested == user['role']:  # Check if the requested role matches the stored role
                if user['role'] == 'admin':
                    return redirect(url_for('admin_ui'))
                elif user['role'] == 'volunteer':
                    return redirect(url_for('volunteer_ui'))
            else:
                flash('Invalid role.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

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
    
    if 'user_email' not in session:
        flash('You need admin access to post shifts.', 'danger')
        return redirect(url_for('index'))
    
    title = request.form['shift_title']
    start_datetime = request.form['start_datetime']
    end_datetime = request.form['end_datetime']
    description = request.form['description']
    '''
    email = session.get('user_email', None)  # Get the email from session, or None if not logged in
'''
    db = connect_db()
    cur = db.cursor()
    ''''''
    # Check if the email should be recorded at the time of shift creation
    
    cur.execute('INSERT INTO shifts (title, start_time, end_time, description, volunteer_email) VALUES (?, ?, ?, ?, NULL)',
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
    cur.execute('SELECT id, title, start_time, end_time, description, volunteer_email FROM shifts')
    shifts = cur.fetchall()  # Make sure this query is correctly fetching the latest data
    db.close()
    return render_template('volunteer_ui.html', shifts=shifts, user_email=session.get('user_email', ''))

def init_db():
    db = connect_db()
    cur = db.cursor()
    
    # Recreate the tables
    cur.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT,
            signed_up INTEGER DEFAULT 0,
            volunteer_email TEXT)
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hours (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            shift_id INTEGER,
            hours_worked REAL NOT NULL)
    ''')
    db.commit()
    db.close()




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
    

@app.route('/signup_for_shift/<int:shift_id>', methods=['POST'])
def signup_for_shift(shift_id):
    
    if 'user_email' not in session:
        flash('You need to log in to sign up for shifts.', 'danger')
        return redirect(url_for('index'))
    
    email = session['user_email']
    db = connect_db()
    cur = db.cursor()
    # Update to overwrite the existing volunteer_email, regardless of its current value
    print(f"Attempting to update shift {shift_id} with email {email}")
    cur.execute('UPDATE shifts SET volunteer_email = ? WHERE id = ?', (email, shift_id))
    db.commit()
    print(f"Updated {cur.rowcount} rows")  # This will tell you how many rows were affected by the update

    
    print("hello world") #for debugging

    
    # Check if the update was successful
    if cur.rowcount == 0:
        flash('No such shift exists.', 'danger')
    else:
        flash('You have successfully signed up for the shift.', 'success')
    
    return redirect(url_for('volunteer_ui'))



# Route for the administrator interface to manage hours
@app.route('/manage_hours')
def manage_hours():
    db = connect_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM hours ORDER BY entry_id DESC')
    logged_hours = cur.fetchall()
    db.close()
    return render_template('manage_hours.html', logged_hours=logged_hours)

@app.route('/clear_hours', methods=['POST'])
def clear_hours():
    db = connect_db()
    cur = db.cursor()
    cur.execute('DELETE FROM hours')  # This will clear the entire table
    db.commit()
    db.close()
    flash('All hours have been cleared.', 'success')
    return redirect(url_for('manage_hours'))

@app.route('/shifts')
def view_shifts():
    db = connect_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM shifts')
    shifts = cur.fetchall()
    db.close()
    return render_template('view_shifts.html', shifts=shifts)

@app.route('/delete_shift/<int:shift_id>', methods=['POST'])
def delete_shift(shift_id):
    db = connect_db()
    cur = db.cursor()
    cur.execute('DELETE FROM shifts WHERE id = ?', (shift_id,))
    db.commit()
    db.close()
    flash('Shift deleted successfully.', 'success')
    return redirect(url_for('view_shifts'))


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

from email_service import send_email

from flask import render_template, request, redirect, url_for

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        affiliation = request.form.get('affiliation')
        donation_type = request.form.getlist('donation_type')  # Using getlist to handle checkboxes
        dedicated_amount = request.form.get('dedicated_amount', '')
        dedicated_items = request.form.get('dedicated_items', '')
        phone = request.form.get('phone', '')  # Capture phone number

        # Prepare the email body with all information
        body = f"""
        New donation from:
        Name: {name}
        Email: {email}
        Phone: {phone}  
        Affiliation: {affiliation}
        Donation Type: {', '.join(donation_type)}
        Dedicated Amount: {dedicated_amount}
        Dedicated Items: {dedicated_items}
        """

        # Sending the email
        send_email("New Donation Received",
                   sender=app.config['MAIL_USERNAME'],
                   recipients=["bailebeni01@gmail.com"],
                   body=body)

        return redirect(url_for('thank_you'))
    else:
        # Load the donation form on GET request
        return render_template('donate.html')


@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')
@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Remove the user email from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/return_volunteer')
def return_volunteer():
    return redirect(url_for('volunteer_ui'))

@app.route('/return_admin')
def return_admin():
    return redirect(url_for('admin_ui'))

if __name__ == '__main__':
    init_db()  # This will ensure the database schema is up-to-date
    app.run(debug=True, host='0.0.0.0', port=5003)