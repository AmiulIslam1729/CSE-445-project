import pandas as pd
import pdfplumber
import re

# Define station names in the required order
stations = [
    "Barishal", "Bhola", "Patuakhali", "Chandpur", "Ambagan", "Cumilla", "CoxsBazar", "Feni", "Mcourt",
    "Rangamati", "Dhaka", "Faridpur", "Madaripur", "Tangail", "Mongla", "Chuadanga", "Jashore", "Khulna", "Satkhira",
    "Mymensingh", "Bogura", "Ishwardi", "Rajshahi", "Dinajpur", "Syedpur", "Rangpur", "Srimangal", "Sylhet"
]

# Function to clean data (handle missing values like *, **, or -)
def clean_value(value):
    if value in ["*", "**", "-", ""]:
        return None
    try:
        return float(value)
    except ValueError:
        return None

# Function to extract rainfall data from PDF
def extract_rainfall_data(pdf_path):
    rainfall_data = {
        "Station": [], 
        "2018_November": [], "2018_December": [], "2019_January": [], "2019_February": [],
        "2019_March": [], "2019_April": [], "2019_May": [], "2019_June": []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) < 2:
            print("Error: The PDF should contain at least two pages for 2018 and 2019 data.")
            return pd.DataFrame()
        
        # Extract 2018 and 2019 data
        text_2018 = pdf.pages[0].extract_text()
        text_2019 = pdf.pages[1].extract_text()
        
        if not text_2018 or not text_2019:
            print("Error: Could not extract text from one or both pages.")
            return pd.DataFrame()
        
        def parse_page_data(text, is_2018):
            lines = text.split("\n")
            extracted_data = {}
            
            for line in lines:
                parts = re.split(r'\s+', line.strip())  # Split by spaces
                if len(parts) < 12:  # Ensure there are enough columns
                    continue
                
                station_name = parts[0].strip()
                if station_name in stations:
                    extracted_data[station_name] = [clean_value(parts[i]) for i in range(1, len(parts))]
            
            return extracted_data
        
        data_2018 = parse_page_data(text_2018, is_2018=True)
        data_2019 = parse_page_data(text_2019, is_2018=False)
        
        for station in stations:
            rainfall_data["Station"].append(station)
            
            # Handle cases where data is missing by using .get() with default empty list
            nov_18 = data_2018.get(station, [None] * 12)[10] if station in data_2018 and len(data_2018[station]) > 10 else None
            dec_18 = data_2018.get(station, [None] * 12)[11] if station in data_2018 and len(data_2018[station]) > 11 else None
            
            rainfall_data["2018_November"].append(nov_18)
            rainfall_data["2018_December"].append(dec_18)
            rainfall_data["2019_January"].append(data_2019.get(station, [None]*12)[0])  
            rainfall_data["2019_February"].append(data_2019.get(station, [None]*12)[1])  
            rainfall_data["2019_March"].append(data_2019.get(station, [None]*12)[2])  
            rainfall_data["2019_April"].append(data_2019.get(station, [None]*12)[3])  
            rainfall_data["2019_May"].append(data_2019.get(station, [None]*12)[4])  
            rainfall_data["2019_June"].append(data_2019.get(station, [None]*12)[5])  
    
    df = pd.DataFrame(rainfall_data)
    df = df.drop_duplicates(subset=["Station"]).reset_index(drop=True)
    
    print(df.head())  # Debugging print to check the extracted data
    
    return df

# Function to calculate averages
def calculate_average(row, months):
    values = [row[month] for month in months if pd.notna(row[month])]
    return round(sum(values) / len(values), 2) if values else None  # Handle missing values

# Define the required month ranges
ranges = {
    "Nov18-May19": ["2018_November", "2018_December", "2019_January", "2019_February", "2019_March", "2019_April", "2019_May"],
    "Dec18-June19": ["2018_December", "2019_January", "2019_February", "2019_March", "2019_April", "2019_May", "2019_June"]
}

def process_pdf(pdf_path, output_file):
    df = extract_rainfall_data(pdf_path)
    
    if df.empty:
        print("No valid data extracted. Please check PDF formatting.")
        return

    for name, months in ranges.items():
        df[name] = df.apply(lambda row: calculate_average(row, months), axis=1)
    
    df = df.set_index("Station").reindex(stations).reset_index()
    print(df.head())  # Debugging: Print first few rows to check alignment
    df.to_excel(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Example usage
pdf_path = r"C:\\Users\\Lenovo\\Downloads\\2022 rainfall merged.pdf"
output_file = "boro_rainfall_output_2022.xlsx"

process_pdf(pdf_path, output_file)
