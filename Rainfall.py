import pandas as pd
import pdfplumber
import re

# Define station names in the required order
stations = [
    "Barishal", "Bhola", "Patuakhali", "Chandpur", "Ambagan", "Cumilla", "CoxsBazar", "Feni", "Mcourt",
    "Rangamati", "Dhaka", "Faridpur", "Madaripur", "Tangail", "Mongla", "Chuadanga", "Jashore", "Khulna", "Satkhira",
    "Mymensingh", "Bogura", "Ishwardi", "Rajshahi", "Dinajpur", "Syedpur", "Rangpur", "Srimangal", "Sylhet"
]

# Function to extract rainfall data from PDF
def extract_rainfall_data(pdf_path):
    rainfall_data = {"Station": [], "March": [], "April": [], "May": [], "June": [], "July": [], "August": [], "September": [], "October": [], "November": [], "December": []}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    parts = re.split(r'\s+', line.strip())
                    station_name = parts[0].strip()  # Clean station names
                    
                    if station_name in stations and station_name not in rainfall_data["Station"]:  # Avoid duplicates
                        try:
                            rainfall_data["Station"].append(station_name)
                            extracted_values = [
                                float(parts[i]) if i < len(parts) and re.match(r"^\d+(\.\d+)?$", parts[i]) else None
                                for i in range(3, 13)
                            ]
                            
                            # Ensure row has exactly 10 values (March to December)
                            while len(extracted_values) < 10:
                                extracted_values.append(None)
                            
                            for month, value in zip(["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], extracted_values):
                                rainfall_data[month].append(value)
                        except (IndexError, ValueError):
                            print(f"Skipping invalid data line: {line}")
    
    df = pd.DataFrame(rainfall_data)
    
    # Drop any duplicate station names
    df = df.drop_duplicates(subset=["Station"])
    
    return df

# Function to calculate averages
def calculate_average(row, months):
    values = [row[month] for month in months if month in row and pd.notna(row[month])]
    return round(sum(values) / len(values), 2) if values else None  # Handle missing data safely, round to 2 decimal places

# Define the required month ranges
ranges = {
    "March-August": ["March", "April", "May", "June", "July", "August"],
    "June-December": ["June", "July", "August", "September", "October", "November", "December"],
    "March-December": ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
}

def process_pdf(pdf_path, output_file):
    df = extract_rainfall_data(pdf_path)
    
    for name, months in ranges.items():
        df[name] = df.apply(lambda row: calculate_average(row, months), axis=1)
    
    # Ensure all station names are included (fill missing ones with NaN)
    df = df.set_index("Station").reindex(stations).reset_index()
    
    # Save the output to an Excel file
    df[["Station", "March-August", "June-December", "March-December"]].to_excel(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Example usage
pdf_path = r"C:\\Users\\Lenovo\\Downloads\\2022 rainfall.pdf"  # Your actual file path
output_file = "rainfall_output_2022.xlsx"
process_pdf(pdf_path, output_file)