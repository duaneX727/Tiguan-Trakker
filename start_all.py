
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# 1. Define paths relative to the script location
    # Go up two levels: Tiguan-Project -> K10-Lab -> lab-server
base_dir = Path(__file__).resolve().parent
lab_server_dir = base_dir.parent.parent
    
node_dir = lab_server_dir / "trakker-ingest-webhook"
py_server = lab_server_dir / "trakker-analytics-api" / "server.py"


# Access the token
CLOUDFLARE_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

# Example usage (e.g., in headers for an API request)
headers = {
    "Authorization": f"Bearer {CLOUDFLARE_TOKEN}",
    "Content-Type": "application/json"
}

# Load environment variables from the .env file in the same directory
load_dotenv()

# Get the directory where this script is located
base_dir = Path(__file__).resolve().parent
    # Go UP two folder levels to reach lab-server
lab_server_dir = base_dir.parent.parent
    
def run_services():
        # Define paths using the lab_server_dir
        node_dir = lab_server_dir / "trakker-ingest-webhook"
        py_server = lab_server_dir / "trakker-analytics-api" / "server.py"
    
    # 2. Start Node.js server
    # We use 'cwd=node_dir' to ensure Node runs inside the folder where server.js lives
print("Starting Node.js server...")
node_proc = subprocess.Popen(["node", "server.js"], cwd=node_dir)

    # 3. Start Python server
print("Starting Python analytics server...")
try:
        # This keeps the Python server in the foreground
        # Use sys.executable to ensure we use the same Python interpreter as the current venv
        subprocess.run([sys.executable, str(py_server)])
except KeyboardInterrupt:
        print("\nShutting down services...")
        # Terminate the background Node process when we exit the Python script
        node_proc.terminate()

if __name__ == "__main__":
    run_services()