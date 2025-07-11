import sqlite3

def init_db():
    conn = sqlite3.connect('data/expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount FLOAT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            is_fraud BOOLEAN DEFAULT FALSE
        )
    ''')
    sample_data = [
        (100.50, '2025-07-01', 'Office Supplies', False),
        (5000.00, '2025-07-02', 'Travel Expense', True),
        (75.25, '2025-07-03', 'Lunch Meeting', False),
        (100.50, '2025-07-04', 'Office Supplies', True),
    ]
    cursor.executemany('INSERT INTO expenses (amount, date, description, is_fraud) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
