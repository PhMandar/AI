from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def execute_query(query, vars):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query, vars)
        result = None
        if cur.description:
            result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"DB Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    action = data.get("action")
    payload = data.get("data")

    print(f"Action: {action}, Payload: {payload}")  # Debugging statement

    if action == "CREATE_PATIENT":
        # Returns ID and confirms name
        res = execute_query("INSERT INTO patients (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id", (payload,))
        p_id = res[0] if res else None
        return jsonify({"status": "success", "patient_id": p_id, "name": payload})

    if action == "FETCH_DATES":
        # Get Patient Name + Last 5 Record Dates
        patient = execute_query("SELECT name FROM patients WHERE id = %s", (payload,))
        if not patient: return jsonify({"status": "error", "message": "ID not found"})
        
        dates = []
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT recorded_at::date, id FROM vitals WHERE patient_id = %s ORDER BY recorded_at DESC LIMIT 5", (payload,))
            dates = [{"date": str(r[0]), "id": r[1]} for r in cur.fetchall()]
            cur.close()
            conn.close()
        except: pass
        return jsonify({"status": "success", "name": patient[0], "dates": dates})

    if action == "FETCH_SPECIFIC_VITAL":
        # Get details for a specific record ID
        row = execute_query("SELECT bp, oxygen, pulse, temperature, weight, height FROM vitals WHERE id = %s", (payload,))
        keys = ['bp', 'oxygen', 'pulse', 'temp', 'weight', 'height']
        return jsonify({"status": "success", "vitals": dict(zip(keys, row))})

    if action == "SAVE_VITALS":
        p_id = data.get("patient_id")
        v = payload # Dictionary of vitals
        execute_query("""
            INSERT INTO vitals (patient_id, bp, oxygen, pulse, temperature, weight, height) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (p_id, v['bp'], v['oxygen'], v['pulse'], v['temp'], v['weight'], v['height']))
        return jsonify({"status": "success", "message": "Vitals saved successfully!"})
    
    if action == "FETCH_PATIENT":
        p_id = payload
        # 1. Get Patient Name
        patient = execute_query("SELECT name FROM patients WHERE id = %s", (p_id,))
        if not patient:
            return jsonify({"status": "error", "message": "Patient ID not found."})
        
        # 2. Get All Vitals for this ID
        vitals_rows = []
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("""
                SELECT bp, oxygen, pulse, temperature, weight, height, recorded_at 
                FROM vitals WHERE patient_id = %s ORDER BY recorded_at DESC
            """, (p_id,))
            vitals_rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error fetching vitals: {e}")

        # Format rows for JSON
        history = []
        for v in vitals_rows:
            history.append({
                "bp": v[0], "oxygen": v[1], "pulse": v[2],
                "temp": v[3], "weight": v[4], "height": v[5],
                "date": v[6].strftime("%Y-%m-%d %H:%M")
            })

        return jsonify({
            "status": "success", 
            "name": patient[0], 
            "history": history
        })

    return jsonify({"status": "error"})


if __name__ == '__main__':
    app.run(debug=True)
