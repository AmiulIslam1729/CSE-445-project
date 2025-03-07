import pdfplumber
import pandas as pd

# Define input PDF and output Excel file
pdf_path = "C:\\Users\\Lenovo\\Downloads\\2017 Crop.pdf"  # Use your actual PDF file path
output_excel = "rice_yield_2017.xlsx"

# List of required regions (lowercased for better matching)
required_regions = {
    "Dhaka", "Tangail", "Mymensingh", "Mymenshing", "Faridpur", "Madaripur", "Hobigonj", "Sylhet", "Bogura", "Bogra",
    "Dinajpur", "Pabna", "Rajshahi", "Rangpur", "Nilphamari", "Chuadanga", "Jessore", "Jashore", "Khulna", "Bagerhat", 
    "Satkhira", "Barishal", "Bhola", "Patuakhali", "Chandpur", "Chattogram", "Cumilla", "Cox's Bazar", "Feni", 
    "Noakhali", "Rangamati"
}

# Define the desired station order
station_order = [
    "Barishal", "Bhola", "Patuakhali", "Chandpur", "Chattogram", "Cumilla", "Cox' Bazar", "Feni", "Noakhali", "Rangamati",
    "Dhaka", "Faridpur", "Madaripur", "Tangail", "Bagerhat", "Chuadanga", "Jashore", "Khulna", "Satkhira",
    "Mymensingh", "Bogura", "Pabna", "Rajshahi", "Dinajpur", "Nilphamari", "Rangpur", "Hobigonj", "Sylhet"
]

# Initialize a list to store extracted data
data = []

# Open the PDF and extract tables till page 18
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages[:18]):  # Only process pages 1 to 18
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if row and len(row) > 0 and row[0]:  # Ensure row is valid and not empty
                    station_name = row[0].strip().lower()  # Normalize case and remove spaces
                    if any(region in station_name for region in required_regions):  
                        data.append(row)

# **Debugging Step: Print extracted data preview**
if data:
    print("Extracted Data Preview:", data[:5])  # Print first 5 rows to verify
else:
    print("No matching data found. Check station name format.")

# Convert extracted data into a DataFrame
df = pd.DataFrame(data)

# Ensure at least one valid row was extracted
if df.empty:
    print("Error: No valid data extracted. Check PDF format or station names.")
else:
    # Rename first column to "Station" if it exists
    if 0 in df.columns:
        df.rename(columns={0: "Station"}, inplace=True)

    # Ensure correct sorting order if "Station" exists
    if "Station" in df.columns:
        df["Station"] = df["Station"].str.strip()  # Remove extra spaces
        df["Station"] = pd.Categorical(df["Station"], categories=station_order, ordered=True)
        df = df.sort_values(by="Station").reset_index(drop=True)

        # Save the extracted data to an Excel file
        df.to_excel(output_excel, index=False, header=False)
        print(f"Filtered data saved to {output_excel}")
    else:
        print("Error: 'Station' column not found. Check extracted data format.")
