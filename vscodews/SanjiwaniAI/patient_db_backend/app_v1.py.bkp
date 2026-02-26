from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

# Database connection configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def save_to_db(text):
    try:
        print("Attempting to connect to the database...")  # Debugging statement
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO user_vault (content) VALUES (%s)", (text,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_message():
    print("Received data:", request.json)  # Debugging statement
    data = request.json
    user_input = data.get("text", "").lower()
    
    # Logic to handle storage
    if user_input:
        success = save_to_db(user_input)
        print("Database save success:", success)  # Debugging statement
        if success:
            return jsonify({"reply": "Data has been saved. I am going back to sleep."})
    
    return jsonify({"reply": "I couldn't save that. Try again?"})

if __name__ == '__main__':
    app.run(debug=True)
