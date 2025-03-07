import pandas as pd
import pdfplumber
import re

# Define station names in the required order
stations = [
    "Barishal", "Bhola", "Patuakhali", "chandpur", "Ambagan(Ctg)", "Cumilla", "CoxsBazar", "Feni", "Mcourt",
    "Rangamati", "Dhaka", "Faridpur", "Madaripur", "Tangail", "Mongla", "Chuadanga",  "Jashore", "Khulna", "Satkhira",
    "Mymensingh", "Bogura", "Ishwardi", "Rajshahi", "Dinajpur", "Syedpur", "Rangpur", "Srimangal", "Sylhet"
]

# Function to extract temperature data from PDF

def extract_temperature_data(pdf_path):
    temperature_data = {"Station": [], "2016_November": [], "2016_December": [], "2017_January": [], "2017_February": [], "2017_March": [], "2017_April": [], "2017_May": [], "2017_June": []}
    
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) < 2:
            print("Error: The PDF should contain at least two pages for 2016 and 2017 data.")
            return pd.DataFrame()
        
        # Extract 2016 and 2017 data from respective pages
        text_2016 = pdf.pages[0].extract_text()
        text_2017 = pdf.pages[1].extract_text()
        
        if not text_2016 or not text_2017:
            print("Error: Could not extract text from one or both pages.")
            return pd.DataFrame()
        
        def parse_page_data(text):
            lines = text.split("\n")
            extracted_data = {}
            
            for line in lines:
                parts = re.split(r'\s+', line.strip())  # Split by spaces
                if len(parts) >= 14 and parts[0] in stations:  # Ignore Year column
                    extracted_data[parts[0]] = [float(parts[i]) if re.match(r"^\d+(\.\d+)?$", parts[i]) else None for i in range(2, 14)]  # Ignore Year column (index 1)
            return extracted_data
        
        data_2016 = parse_page_data(text_2016)
        data_2017 = parse_page_data(text_2017)
        
        for station in stations:
            temperature_data["Station"].append(station)
            temperature_data["2016_November"].append(data_2016.get(station, [None]*12)[10])  # 11th column
            temperature_data["2016_December"].append(data_2016.get(station, [None]*12)[11])  # 12th column
            temperature_data["2017_January"].append(data_2017.get(station, [None]*12)[0])  # 1st column
            temperature_data["2017_February"].append(data_2017.get(station, [None]*12)[1])  # 2nd column
            temperature_data["2017_March"].append(data_2017.get(station, [None]*12)[2])  # 3rd column
            temperature_data["2017_April"].append(data_2017.get(station, [None]*12)[3])  # 4th column
            temperature_data["2017_May"].append(data_2017.get(station, [None]*12)[4])  # 5th column
            temperature_data["2017_June"].append(data_2017.get(station, [None]*12)[5])  # 6th column
    
    df = pd.DataFrame(temperature_data)
    df = df.drop_duplicates(subset=["Station"]).reset_index(drop=True)
    return df

# Function to calculate averages
def calculate_average(row, months):
    values = [row[month] for month in months if month in row and pd.notna(row[month])]
    return round(sum(values) / len(values), 2) if values else None

# Define the required month ranges
ranges = {
    "Nov16-May17": ["2016_November", "2016_December", "2017_January", "2017_February", "2017_March", "2017_April", "2017_May"],
    "Dec16-June17": ["2016_December", "2017_January", "2017_February", "2017_March", "2017_April", "2017_May", "2017_June"]
}

def process_pdf(pdf_path, output_file):
    df = extract_temperature_data(pdf_path)
    
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
pdf_path = r"C:\\Users\\Lenovo\\Downloads\\2022 temp merged.pdf"
output_file = "boro_temperature_output_2022.xlsx"
process_pdf(pdf_path, output_file)