import pdfplumber
import pandas as pd

# Define input PDF and output Excel file
pdf_path = "C:\\Users\\Lenovo\\Downloads\\2015 crops.pdf"  # Replace with your actual PDF file path
output_excel = "rice_yield_2015.xlsx"

# List of required regions
required_regions = {
    "Dhaka", "Tangail","Tangail Region","Tangail Region", "Mymensingh","Mymenshing", "Faridpur", "Madaripur", "Hobigonj", "Sylhet", "Bogura","Bogra", "Dinajpur", 
     "Pabna", "Rajshahi", "Rangpur", "Nilphamari", "Chuadanga", "Jessore", "Jashore", "Khulna", "Bagerhat", "Satkhira", 
    "Barisal", "Bhola", "Patuakhali", "Chandpur","Chittagong", "Comilla", 
    "Cox's Bazar", "Feni", "Noakhali", "Rangamati"
}

# Initialize a list to store extracted data
data = []

# Open the PDF and extract tables till page 18
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[:18]:  # Only process pages 1 to 18
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if any(region in row for region in required_regions):
                    data.append(row)

# Convert extracted data into a DataFrame
df = pd.DataFrame(data)

# Save the extracted data to an Excel file
df.to_excel(output_excel, index=False, header=False)

print(f"Filtered data saved to {output_excel}")
