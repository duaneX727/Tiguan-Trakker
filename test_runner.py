import pandas as pd
# Import your actual cleaning functions
try:
    from clean_logs import process_vehicle_data # Change to your actual function name
    from clean_logs_v3 import process_vehicle_logs
except ImportError:
    print("Could not import clean_logs. Ensure the filenames match.")
    print("Could not import clean_logs_v3. Ensure the filenames match.")

def run_tests():
    print("--- Starting Test Run ---")
    
    # 1. Load the generated messy data
    df_raw = pd.read_csv("test_logs_input.csv")
    print(f"Initial Rows: {len(df_raw)}")
    test_file = "test_logs_input.csv"
    print(f"Testing with file: {test_file}")

    # 2. Run your cleaning logic
    # Replace this with your actual processing call
    df_clean = process_vehicle_data(df_raw) 
    # 1. Run your cleaning logic (v3 takes a file path, not a dataframe)
    df_clean = process_vehicle_logs(test_file) 

    # 3. VALIDATION CHECKS
    if df_clean is None:
        print("❌ FAIL: process_vehicle_logs returned None. Check the input file.")
        return

    # 2. VALIDATION CHECKS
    
    # Test: Duplicate Removal
    if len(df_clean[df_clean.duplicated(subset=['Date', 'Odometer'])]) == 0:
        print("✅ SUCCESS: Duplicates removed.")
    else:
        print("❌ FAIL: Duplicates still exist.")

    # Test: Date Parsing
    # Check if '04/22/2026' became a proper datetime object
    # Test: Date Parsing (v3 forces 'YYYY-MM-DD' string format)
    sample_date = df_clean.iloc[2]['Date'] 
    if not isinstance(sample_date, str):
    if isinstance(sample_date, str) and len(sample_date) == 10 and sample_date.count('-') == 2:
        print(f"✅ SUCCESS: Date format parsed correctly ({sample_date})")
    else:
        print("❌ FAIL: Date is still a string.")
        print(f"❌ FAIL: Date format is incorrect or still raw string: {sample_date}")

    # Test: Missing Values
    if df_clean['Gallons'].isnull().sum() == 0:
        print("✅ SUCCESS: Empty values handled/removed.")
    # Test: Partial Fill Logic (MPG > 33 rule)
    if 'Fill_Type' in df_clean.columns:
        partial_fills = df_clean[df_clean['Fill_Type'] == 'Partial']
        if not partial_fills.empty:
            print(f"✅ SUCCESS: Partial fills detected correctly ({len(partial_fills)} found).")
        else:
            print("⚠️ WARNING: No partial fills detected. Does the test CSV have an MPG > 33?")
    else:
        print("⚠️ WARNING: Script kept rows with missing Gallons.")
        print("❌ FAIL: 'Fill_Type' column is missing. Partial fill logic failed.")

    print(f"Final Cleaned Rows: {len(df_clean)}")
    print("--- Test Run Complete ---")

if __name__ == "__main__":
    run_tests()