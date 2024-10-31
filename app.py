from flask import Flask, request, render_template, redirect, url_for
import requests
import pandas as pd
import sqlite3

app = Flask(__name__)

DATABASE = 'data.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the database and table if they don't exist
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT,
                event_type TEXT,
                product_problems TEXT,
                date_received TEXT
            )
        ''')
        conn.commit()

# Fetch data from openFDA API
def fetch_API(query):
    response = requests.get(query)
    if response.status_code == 200:
        data = response.json().get('results', [])
        return data
    else:
        return None

# Normalize and save data to SQLite
def save_to_db(data):
    combined_data = pd.json_normalize(data)
    with get_db_connection() as conn:
        for _, row in combined_data.iterrows():
            conn.execute('''
                INSERT INTO events (brand_name, event_type, product_problems, date_received)
                VALUES (?, ?, ?, ?)
            ''', (
                row['device'][0]['brand_name'] if isinstance(row['device'], list) and row['device'] else None,
                row['event_type'],
                '; '.join(row['product_problems']) if isinstance(row['product_problems'], list) else None,
                row['date_received']
            ))
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_code = request.form['product_code']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        query = f"https://api.fda.gov/device/event.json?search=date_received:[{start_date}+TO+{end_date}]+AND+device.device_report_product_code.exact:{product_code}&limit=500"
        
        data = fetch_API(query)
        
        if data:
            save_to_db(data)  # Save data to the database
            return redirect(url_for('results'))
        else:
            return render_template('index.html', error="No results found or an error occurred.")

    return render_template('index.html')

@app.route('/results')
def results():
    with get_db_connection() as conn:
        events = conn.execute('SELECT * FROM events').fetchall()
    return render_template('results.html', events=events)

@app.route('/reports')
def reports():
    with get_db_connection() as conn:
        # Query for event counts by brand and event type
        event_counts = conn.execute('''
            SELECT brand_name, event_type, COUNT(*) as count
            FROM events
            GROUP BY brand_name, event_type
            ORDER BY brand_name, count DESC
        ''').fetchall()

        # Query for product problems counts by brand
        problem_counts = conn.execute('''
            SELECT brand_name, product_problems, COUNT(*) as count
            FROM events
            GROUP BY brand_name, product_problems
            ORDER BY brand_name, count DESC
        ''').fetchall()

    return render_template('reports.html', event_counts=event_counts, problem_counts=problem_counts)

if __name__ == "__main__":
    init_db()  # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=5000)
