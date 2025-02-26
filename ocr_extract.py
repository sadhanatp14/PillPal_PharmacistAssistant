import pytesseract
import re

# Load the preprocessed image
image_path = "processed.jpg"

# Use Tesseract for OCR
custom_config = r'--oem 3 --psm 11'  # Best mode for text blocks
extracted_text = pytesseract.image_to_string(image_path, config=custom_config)

# Post-processing to clean the text
def clean_ocr_text(text):
    text = text.replace("\n", " ")  # Remove new lines
    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)  # Remove special characters
    text = re.sub(r'\bremdec\b', 'Remdesivir', text, flags=re.IGNORECASE)  # Correct common misreading
    return text

cleaned_text = clean_ocr_text(extracted_text)

print("🔹 Extracted Text:\n", cleaned_text)
