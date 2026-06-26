import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def run_services():
    # 100% explicitly mapped paths to your lab-server layout
    node_dir = r"C:\mdmcode\lab-server\trakker-ingest-webhook"
    py_server_file = r"C:\mdmcode\lab-server\trakker-analytics-api\server.py"

    print("=" * 60)
    print("🚀 INITIALIZING PRODUCTION MASTER K10 LAB INFRASTRUCTURE")
    print("=" * 60)

    # 1. Launch Edge Network Tunnel
    print("[+] Starting Cloudflare Tunnel (Protocol: HTTP/2)...")
    tunnel_cmd = ["cloudflared", "tunnel", "run", "--protocol", "http2", "mdm-api-server"]
    tunnel_proc = subprocess.Popen(tunnel_cmd)

    # 2. Launch Ingest Webhook Engine
    print(f"[+] Starting Node.js webhook server from: {node_dir}")
    node_proc = subprocess.Popen(["node", "server.js"], cwd=node_dir)

    # 3. Launch Analytics Engine
    print(f"[+] Starting Python analytics server file: {py_server_file}")
    print("=" * 60)
    
    try:
        py_dir = str(Path(py_server_file).parent)
        # Using subprocess.Popen instead of .run so it doesn't block the execution stream
        py_proc = subprocess.Popen([sys.executable, py_server_file], cwd=py_dir)
        
        # Keep the master orchestrator alive to hold open the background process threads
        py_proc.wait()
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 SHUTTING DOWN MASTER LAB SERVICES CLEANLY...")
        print("=" * 60)
        
        node_proc.terminate()
        tunnel_proc.terminate()
        py_proc.terminate()
        
        node_proc.wait()
        tunnel_proc.wait()
        py_proc.wait()
        print("[✓] Core laboratory threads safely terminated.")

if __name__ == "__main__":
    run_services()