from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to connect to the database
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
@app.route('/admin/manage_hours')
def manage_hours():
    db = connect_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM hours')
    logged_hours = cur.fetchall()
    db.close()
    return render_template('manage_hours.html', logged_hours=logged_hours)

if __name__ == '__main__':
    app.run(debug=True)
