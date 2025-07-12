import os
import sqlite3
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, amount REAL, date TEXT, description TEXT, is_fraud INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO expenses (amount, date, description, is_fraud) VALUES (100.50, '2025-07-01', 'Office Supplies', 0)")
    cursor.execute("INSERT OR IGNORE INTO expenses (amount, date, description, is_fraud) VALUES (250.00, '2025-07-02', 'Travel', 1)")
    cursor.execute("INSERT OR IGNORE INTO expenses (amount, date, description, is_fraud) VALUES (75.25, '2025-07-03', 'Lunch', 0)")
    cursor.execute("INSERT OR IGNORE INTO expenses (amount, date, description, is_fraud) VALUES (500.00, '2025-07-04', 'Equipment', 1)")
    conn.commit()
    conn.close()

init_db()  # Initialize database on app start

@app.route('/')
def home():
    return "Expense Fraud Detector API is running. Use /predict with POST."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'amount' not in data or 'date' not in data or 'description' not in data:
        return jsonify({'error': 'Missing required fields (amount, date, description)'}), 400
    
    import pandas as pd
    new_df = pd.DataFrame([data])
    new_df['date'] = pd.to_datetime(new_df['date'])
    df = pd.read_sql_query("SELECT * FROM expenses", sqlite3.connect('data/expenses.db'))
    min_date = pd.to_datetime(df['date'].min())
    new_df['days_since'] = (new_df['date'] - min_date).dt.days
    new_df['desc_length'] = new_df['description'].str.len()
    X_new = new_df[['amount', 'days_since', 'desc_length']]
    
    # Load the pre-trained model
    model = joblib.load('fraud_detector.pkl')  # Ensure this file is in the repo
    prediction = model.predict(X_new)[0]
    return jsonify({'is_fraud': bool(prediction)})
