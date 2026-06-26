import os
import subprocess

# Path to the folder containing your entry files
import_dir = 'import_data'

for filename in os.listdir(import_dir):
    if filename.endswith('.txt'):
        with open(os.path.join(import_dir, filename), 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            # Unpack the lines: date, odo, trip, gal, price
            date, odo, trip, gal, price = lines
            
            # Execute the command
            cmd = ["python", "db_manager.py", "--add", date, odo, trip, gal, price]
            subprocess.run(cmd)
            print(f"Ingested {filename}")