import os
import sys
import sqlite3
import argparse
import pandas as pd

# Configuration
DB_NAME = "tiguan_data.db"

def process_and_load(file_path):
   # Load the raw CSV data directly into a DataFrame
    df = pd.read_csv(file_path, names=['date', 'odometer', 'trip', 'gallons', 'cost', 'notes'])

    # 2. TRANSFORM: Cleaning and Validation
    df['date'] = pd.to_datetime(df['date'])
    
    # Clean the numeric columns first
    numeric_cols = ['odometer', 'trip', 'gallons', 'cost']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate MPG dynamically before filtering
    df['mpg'] = df['trip'] / df['gallons']

    # 3. Apply the "Partial Fill" Rule
    clean_df = df[(df['mpg'] <= 33) | (df['mpg'].isna())].copy()
    # 4. LOAD: Connect to the DB and Save
    conn = sqlite3.connect(os.path.join(os.path.dirname(file_path), DB_NAME))
    clean_df.to_sql('fuel_logs', conn, if_exists='append', index=False)
    conn.close()
    
    print(f"Success: {len(clean_df)} records loaded into {DB_NAME}.")

if __name__ == "__main__":
    # Check if Node passed the file path argument from the command line
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        process_and_load(target_path)
    else:
        print("Error: No file path provided to ETL pipeline.")