# PillPal_PharmacistAssistant
#  Pharmacist’s Assistant
An AI-powered system to automate prescription processing and medicine stock matching using OCR and machine learning.

##  Project Overview
Pharmacist’s Assistant is designed to help pharmacists by automating prescription reading and stock matching.  
This system extracts medicine details from **printed prescriptions using OCR (Google Cloud Vision)** and checks for availability in the **pharmacy’s stock database**.  
If a medicine is unavailable, the system **suggests alternative drugs**, making pharmacy operations more efficient.  

##  Key Features
**AI-powered OCR Processing** – Reads and extracts medicine details from prescriptions.  
**Medicine Stock Matching** – Checks availability in the pharmacy database.  
**Alternative Medicine Suggestions** – Recommends substitutes if the prescribed medicine is out of stock.  
**Interactive User Interface** – User-friendly web interface for pharmacists.  
**Secure API & Data Handling** – Protects prescription details with minimal data storage.  

---

##  Tech Stack
| **Component**   | **Technology Used** |
|----------------|------------------|
| **Frontend**   | React.js, Bootstrap |
| **Backend**    | Flask (Python) |
| **OCR Processing** | Google Cloud Vision API |
| **Database**   | CSV (for stock storage) |
| **Deployment** | Docker (future scope: AWS/GCP/Azure) |

---

## Folder Structure
 Pharmacist-Assistant ┣  backend ┃ ┣  app.py # Flask backend API ┃ ┣  requirements.txt # Python dependencies ┣ frontend ┃ ┣  src/ # React components ┃ ┣ package.json # Frontend dependencies ┣ README.md # This file ┣  .gitignore # Ignore unnecessary files ┣  LICENSE # Open-source license


---

## Installation & Setup
### Clone the Repository  
```bash
git clone https://github.com/sadhanatp14/Pharmacist-Assistant.git
cd Pharmacist-Assistant

---

## Set Up a Virtual Environment
python3 -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate  # Windows

## Install Backend Dependencies
pip install -r requirements.txt

## Start the Flask Backend
cd backend
python app.py

## Install Frontend Dependencies & Start React
cd frontend
npm install
npm start

## API Endpoints (Flask Backend)
Method     	Endpoint     Description
POST	     /upload	     Uploads a prescription image and extracts medicine details.
GET	     /medicines	     Fetches the list of available medicines in stock.
POST	     /order	       Places an order for a prescription.

## Security & Privacy Considerations
Minimal Data Storage – Only necessary prescription details are processed.
Secure API Access – JWT authentication to prevent unauthorized access.
Role-Based Access – Pharmacists can access and process orders securely.
Prescription Image Handling – Secure uploads with automatic deletion after processing.

## Future Enhancements
Medication Reminders – Notify patients about their medicine schedule.
Pill Recognition – Identify pills using a smartphone camera.
Drug Interaction Alerts – Warn users about harmful medicine combinations.
Secure Medical History Storage – Store and retrieve patient records securely.
Cloud Deployment – Deploy using AWS/GCP/Azure for scalability.
Multi-Language OCR – Support prescriptions in different languages.

## License
This project is licensed under the MIT License – free to use, modify, and distribute.

## Contributors
Sadhana TP – GitHub

References & Data Sources
Google Cloud Vision API – Documentation - https://console.cloud.google.com/welcome/new?project=pharmacistassistant-452016
Sample Prescription Dataset – Kaggle - https://www.kaggle.com/datasets/mehaksingal/illegible-medical-prescription-images-dataset
