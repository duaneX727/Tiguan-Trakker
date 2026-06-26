import os
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allows your frontend UI components to connect without CORS errors

# Hardcoded absolute paths to guarantee it locks into your master data directory
DATA_DIR = Path(r"C:\mdmcode\lab-server\K10-Lab\Tiguan-Project\data")
LOG_FILE = DATA_DIR / "raw_logs.csv"


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """
    Parses the raw CSV telemetry logs and calculates live performance metrics.
    """
    if not LOG_FILE.exists():
        return jsonify({
            "status": "error",
            "message": f"Telemetry database not found at {LOG_FILE}. Awaiting initial ingest stream."
        }), 404

    try:
        # Load telemetry data using Pandas
        df = pd.read_csv(LOG_FILE)
        
        if df.empty:
            return jsonify({
                "status": "success",
                "total_records": 0,
                "metrics": {}
            })

        # Calculate live lab metrics
        total_records = len(df)
        
        # Safely extract matching columns if they exist in your schema
        latest_entries = df.tail(10).to_dict(orient='records')

        return jsonify({
            "status": "success",
            "total_records": total_records,
            "latest_telemetry": latest_entries,
            "engine_status": "ONLINE"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to parse analytical metrics: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Core infrastructure heartbeat check.
    """
    return jsonify({
        "status": "healthy",
        "gateway": "K10-Lab Analytics Engine",
        "database_connected": LOG_FILE.exists()
    }), 200


if __name__ == '__main__':
    # Ensure the master data directory exists before starting up
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("⚡ K10 ANALYTICS ENGINE RUNNING ON PORT 5000")
    print(f"📁 Tracking Data Target: {LOG_FILE}")
    print("=" * 60)
    
    # Run locally on standard port 5000
    app.run(host='127.0.0.1', port=5000, debug=False)
