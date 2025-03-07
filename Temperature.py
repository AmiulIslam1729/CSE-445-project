import pandas as pd
import pdfplumber
import re

# Define station names in the required order
stations = [
    "Barishal", "Bhola", "Patuakhali", "chandpur", "Ambagan(Ctg)", "Cumilla", "Cox's Bazar", "Feni", "M.court",
    "Rangamati", "Dhaka", "Faridpur", "Madaripur", "Tangail", "Mongla", "Chuadanga", "Jashore", "Khulna", "Satkhira",
    "Mymensingh", "Bogura", "Ishwardi", "Rajshahi", "Dinajpur", "Syedpur", "Rangpur", "Srimangal", "Sylhet"
]

# Function to extract temperature data from PDF
def extract_temperature_data(pdf_path):
    temperature_data = {month: [] for month in ["Station", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    parts = re.split(r'\s+', line.strip())
                    
                    if len(parts) < 12:  # Skip invalid lines
                        print(f"Skipping incomplete data line: {line}")
                        continue

                    station_name = parts[0].strip()  # Extract station name
                    
                    if station_name in stations and station_name not in temperature_data["Station"]:  # Avoid duplicates
                        try:
                            temperature_data["Station"].append(station_name)
                            for i, month in enumerate(["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], start=3):
                                if i < len(parts) and re.match(r"^\d+(\.\d+)?$", parts[i]):  # Check if value is numeric
                                    temperature_data[month].append(float(parts[i]))
                                else:
                                    temperature_data[month].append(None)  # Handle missing values
                        except (IndexError, ValueError):
                            print(f"Skipping invalid data line: {line}")

    # Ensure all lists are of equal length
    max_length = len(temperature_data["Station"])
    for key in temperature_data:
        while len(temperature_data[key]) < max_length:
            temperature_data[key].append(None)

    df = pd.DataFrame(temperature_data)

    return df

# Function to calculate averages
def calculate_average(row, months):
    values = [row[month] for month in months if pd.notna(row[month])]
    return round(sum(values) / len(values), 2) if values else None  # Handle missing data safely, round to 2 decimal places

# Define the required month ranges
ranges = {
    "March-August": ["March", "April", "May", "June", "July", "August"],
    "June-December": ["June", "July", "August", "September", "October", "November", "December"],
    "March-December": ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
}

def process_pdf(pdf_path, output_file):
    df = extract_temperature_data(pdf_path)

    for name, months in ranges.items():
        df[name] = df.apply(lambda row: calculate_average(row, months), axis=1)

    # Ensure all station names are included (fill missing ones with NaN)
    df = df.set_index("Station").reindex(stations).reset_index()

    # Save the output to an Excel file
    df[["Station", "March-August", "June-December", "March-December"]].to_excel(output_file, index=False)
    print(f"✅ Processed data saved to {output_file}")

# Example usage
pdf_path = r"C:\\Users\\Lenovo\\Downloads\\2022 temp.pdf"  # Your actual file path
output_file = "temperature_output_2022.xlsx"
process_pdf(pdf_path, output_file)
