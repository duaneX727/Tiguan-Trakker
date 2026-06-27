import os

CSV_FILE = "data/raw_logs.csv"

if not os.path.exists(CSV_FILE):
    print("❌ Cannot find file")
else:
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("\n--- DIAGNOSTIC ROW PRINT ---")
    for index, line in enumerate(lines[:6]):  # look at the first few rows
        line_clean = line.strip()
        if not line_clean:
            print(f"Row {index}: Empty Line")
            continue
        parts = line_clean.split()
        print(f"Row {index} raw text: {repr(line_clean)}")
        print(f"Row {index} split tokens: {parts}\n")
