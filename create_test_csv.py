import csv

def generate_test_data():
    filename = "test_logs_input.csv"
    headers = ["Date", "Odometer", "Gallons", "Price_Per_Gallon", "Total_Spent", "Fuel_Type", "Notes"]
    
    data = [
        # 1. Perfect Row
        ["2026-04-01", "45200", "12.5", "4.15", "51.88", "Premium", "Baseline"],
        # 2. The Partial Fill
        ["2026-04-10", "45550", "5.0", "4.20", "21.00", "Premium", "Partial fill"],
        # 3. THE DUPLICATE (Exact same as row 2)
        ["2026-04-10", "45550", "5.0", "4.20", "21.00", "Premium", "Duplicate Row"],
        # 4. THE MESSY DATE (MM/DD/YYYY)
        ["04/22/2026", "46100", "13.2", "4.05", "53.46", "Premium", "Wrong date format"],
        # 5. MISSING DATA (Empty Gallons)
        ["2026-04-25", "46400", "", "4.10", "", "Premium", "Missing gallons"],
        # 6. ODOMETER REGRESSION (Logic error)
        ["2026-04-28", "45000", "10.0", "4.10", "41.00", "Premium", "Backwards Odo"]
    ]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Successfully created {filename}")

if __name__ == "__main__":
    generate_test_data()