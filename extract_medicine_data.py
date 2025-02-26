import os
import pandas as pd
import re
from rapidfuzz import process

# Load medicine dataset
medicine_df = pd.read_csv("medicine_dataset.csv")  # Update with actual filename
medicine_names = medicine_df["brand_name"].tolist()  # List of medicine brand names

# Define regex patterns for name, age, strength, dosage, and frequency
name_pattern = r"(?i)\b(MR\.|MRS\.|MS\.|Mr\.|Ms\.|Mrs\.)\s+([A-Z]+\s+[A-Z]+)"  # (?i) makes it case-insensitive
age_pattern = r"(\d{1,3})/(M|F)"
strength_pattern = r"(\d+\.?\d*\s?(mg|g|mcg|ml|units|IU|pair|pairs))"
dosage_pattern = r"(tablet|injection|syrup|capsule|ampoule|drop|cream|ointment|patch|solution|suspension|tab|inj|Tab|Tab.|Syrup)"
frequency_pattern = r"(OD|BD|TDS|QID|QHS|PRN|STAT|q\d+h|once daily|twice daily|three times a day|every \d+ hours)"

# Folder containing OCR text files
OCR_FOLDER = r'/Users/sadhanatp/Desktop/Study/Hackathons/Girl Hackathon/PharmacistAssistant/newScript/corrected2'  # Update with actual folder path

# Function to extract name and age
def extract_patient_info(text):
    name_match = re.search(name_pattern, text, re.IGNORECASE)  # Case-insensitive search
    age_match = re.search(age_pattern, text)

    patient_name = name_match.group(0) if name_match else "Unknown"
    patient_age = age_match.group(1) if age_match else "Unknown"

    return patient_name, patient_age

# Function to extract medicine details
def extract_medicine_details(text):
    extracted_data = []
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Apply regex first before fuzzy matching (to improve speed)
        if not re.search(r"\b[A-Za-z]+\b", line):  
            continue  # Skip lines without alphabetic words (likely noise)

        # Match medicine names using fuzzy matching
        matched_med, score = None, 0
        result = process.extractOne(line, medicine_names)
        if result:
            matched_med, score, *_ = result  # Corrected unpacking

        if matched_med and score > 80:  # Confidence threshold
            strength = re.search(strength_pattern, line)
            dosage_form = re.search(dosage_pattern, line, re.IGNORECASE)
            frequency = re.search(frequency_pattern, line, re.IGNORECASE)

            extracted_data.append({
                "medicine_name": matched_med,
                "strength": strength.group(0) if strength else None,
                "dosage_form": dosage_form.group(0) if dosage_form else None,
                "frequency": frequency.group(0) if frequency else None
            })

    return extracted_data

# Process all OCR text files
all_extracted_data = []
for filename in os.listdir(OCR_FOLDER):
    if filename.endswith(".txt"):  # Assuming OCR outputs are text files
        with open(os.path.join(OCR_FOLDER, filename), "r", encoding="utf-8") as file:
            text = file.read()

            # Extract patient name & age
            patient_name, patient_age = extract_patient_info(text)

            # Extract medicine details
            medicines = extract_medicine_details(text)

            # Store data for each medicine with patient details
            for med in medicines:
                med["patient_name"] = patient_name
                med["age"] = patient_age
                all_extracted_data.append(med)

# Save extracted data as CSV
output_df = pd.DataFrame(all_extracted_data)
output_df.to_csv("extracted_patient_medicine_data.csv", index=False)
print("✅ Extracted data saved to extracted_patient_medicine_data.csv")

# Save extracted data as JSON (optional)
output_df.to_json("extracted_patient_medicine_data.json", orient="records", indent=4)
print("✅ Extracted data also saved to extracted_patient_medicine_data.json")