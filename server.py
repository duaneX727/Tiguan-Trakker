from flask import Flask, jsonify
import logging
import csv
import os

app = Flask(__name__)
# --- Logger Suppression ---
# This silences the noisy 'GET' request logs from bots
# while keeping your own error and warning logs visible.
log = logging.getLogger("werkzeug")
log.setLevel(logging.WARNING)

# Dynamically find the path of lab-backend-api folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Go back one step (..), then jump straight into the Tiguan logs folder
# Force the path to look for the file starting from the root of your project
# This assumes server.py is in 'lab-backend-api' and the CSV is in 'K10-Lab/Tiguan-Project'

CSV_FILE = os.path.join(BASE_DIR, 'K10-Lab', 'Tiguan-Project', 'cleaned_tiguan_logs.csv')


def read_logs():
    if not os.path.exists(CSV_FILE):
        return {"error": f"File '{CSV_FILE}' not found on server."}
    
    logs = []
    try:
        # Use latin-1 encoding to safely handle em-dash format styles
        with open(CSV_FILE, mode='r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
        return logs
    except Exception as e:
        return {"error": str(e)}


@app.route('/')
def home():
    return "Tiguan-Trakker Backend Active"
# def home():
#     return jsonify({
#         "status": "online",
#         "project": "Tiguan Trakker Homelab API",
#         "endpoints": {
#             "all_logs": "/api/logs"
#         }
#     })

# You can add your Tiguan-Trakker API logic here
# e.g., @app.route('/log-maintenance', methods=['POST'])
@app.route('/api/logs')
def get_logs():
    data = read_logs()
    return jsonify(data)


# --- Startup Log ---
if __name__ == "__main__":
    print("Starting Tiguan-Trakker Server...")
    # Using 0.0.0.0 makes the server accessible on your local network
    app.run(host='0.0.0.0', port=5000)
