from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import os
from fraud_detector import prepare_data, train_model

app = Flask(__name__)

def load_model():
    df = load_data()
    X, y = prepare_data(df)
    return train_model(X, y)

def load_data():
    conn = sqlite3.connect('data/expenses.db')
    query = "SELECT amount, date, description, is_fraud FROM expenses"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route('/')
def home():
    return "Expense Fraud Detector API is running. Use /predict with POST."

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'amount' not in data or 'date' not in data or 'description' not in data:
            return jsonify({'error': 'Missing required fields (amount, date, description)'}), 400
        
        new_df = pd.DataFrame([data])
        new_df['date'] = pd.to_datetime(new_df['date'])
        df = load_data()
        min_date = pd.to_datetime(df['date'].min())  # Ensure min_date is a datetime
        new_df['days_since'] = (new_df['date'] - min_date).dt.days
        new_df['desc_length'] = new_df['description'].str.len()
        X_new = new_df[['amount', 'days_since', 'desc_length']]
        
        model = load_model()
        prediction = model.predict(X_new)[0]  # Fixed indentation
        return jsonify({'is_fraud': bool(prediction)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get("PORT", 5000))
    # Bind to all interfaces (0.0.0.0) for Render
    app.run(host="0.0.0.0", port=port, debug=False)
