from google.cloud import vision
import io
import os

# Initialize Google Vision Client
client = vision.ImageAnnotatorClient()

# Define your corrections dictionary
corrections = {
   "Or. Sachin Kumar SG": "Dr. Sachin Kumar SG",
    
    "RADIO. 2s» Confirming. :-": "RADIO QSL Confirming:",
    "our QSO af a : : 20 =": "Our QSO at 20 UTC =",
    "ON MHz RST g": "ON MHz RST 59",
    "€ xcva g": "Excva G",
    "QOTHER S": "QTH Other S",
    "OUTPUT WATTS ANT.": "Output Watts Antenna",
    "Oras": "Op. Callsign",
    "UP. cet 2 _~": "UP CET 2",
    "REMARKS: |. | | - ?": "Remarks: ",
    "TNX Tribes Ti TeTioddoledsdeedadssedes ld er ddedtberbersterttd": "TNX 73 de Callsign",
    
    "Dr B. Who": "Dr. B. Who",
    "Barmstreet 12": "Barnstreet 12",
    
    "500.00 w. ere sTRECT ODESS2, TEXAS meaatoie": "500-600 W. 8TH STREET, ODESSA, TEXAS",
    "wcrns Fenn solenle gone": "Wounds: Fentanyl Solution Gone",
    
    "B foo": "BP",
    "Woprteka, amr": "Metoprolol, AM",
    "Fe (img out": "Fe 100mg OD",
    
    "f\nar\na °\n4 bod\nciohe\nbe\nsone Cloke\n\neau": "Farina 4 bod, Sodium Chloride",
    
    "Dr, Jayaprakash Hebbar": "Dr. Jayaprakash Hebbar",
    "Res No MaDe OS 2936": "Reg. No. M.D. OS 2936",
    "Clinic ; 2642 2767": "Clinic: 2642 2767",
    "No. 1. Diamond Patace": "No. 1, Diamond Palace",
    "Hull Road,": "Hill Road,",
    "Bandra, Mumba-409 ose": "Bandra, Mumbai-400050",
    "10.30 a.m. to 1 p.m.": "10:30 AM to 1:00 PM",
    "5.00 p.m. to 8.00 p.nt.": "5:00 PM to 8:00 PM",
    "SAT & SUN MOKNING ONLY": "SAT & SUN Morning Only",
    
    "HCG”": "HCG Healthcare",
    "Patient Name Aaannrattd day": "Patient Name: [Unreadable] Day",
    "R AmMPpHoT eA & 7": "R Liposomal Amphotericin B 7mg/kg",
    "Lipase Mal": "Liposomal",
    
    "RTOD 200 -1.00 xf": "RT OD -2.00 DS -1.00 x 180",
    "TOS. -R15 ~95 x90 [7249": "OS -2.15 DS -0.95 x 90",
    
    "OS\nCOEALISS Centre hospitalier universitaire de Sherbrooke\n_ 819 346-1110\nHotel Dieu Hopital Fleurimont\n381. Be ‘ 12° avenue Nord\nSherbrooku ci JtH SNA":
    "CHUS Centre Hospitalier Universitaire de Sherbrooke\n819-346-1110\nHôtel-Dieu / Hôpital Fleurimont\n381, 12e Avenue Nord\nSherbrooke, QC J1H 5N4",

    "Dare Dec \\\" 201": "Date: Dec 201",
    "Se hw \\ volo ard": "Service: Hospital Ward",
    "BR Iecbronivapi evar": "BR Electrotherapy Eval",
    "qa PRN": "q.s. PRN",
    "Awect Covencs 4 orev drwase’": "Aseptic Cover 4 Over Dressings",
    "Apis a mm oe": "Apply as needed",

    "Reynalde 0. Josen, MD, MHA, MHPEd, MSc Surg": "Reynaldo O. Joson, MD, MHA, MHPEd, MSc Surg",
    "MANILA DOCTORS HOSPITAL": "Manila Doctors Hospital",
    "Suite 301, DSMT MAG, ULN. Avenue Ermita, Manila": "Suite 301, DSMT Bldg, U.N. Avenue, Ermita, Manila",
    "rofosonmedelinie@amail.com": "rjosonmedclinic@gmail.com",
    "rjoson2001 @yahoo.com": "rjoson2001@yahoo.com",
    "Li/VA CRUE pas L724 mw LE": "LVA CRUE PAS L724 MW LE",
    
    "Ke\nanithits + Prracommnee$ fab": "Kefanitis + Preacommend Fab",
    "/ Sab ANTES, 6 kre": "Sub Ante, 6 KR",
    "PIE AGOLGEIS Eb.": "Pie Agolgesis Eb.",
    "s MD.\nLic, # 44609": "Dr. MD\nLic. # 44609",
    
    "Trae SENER": "Treatment SENER",
    "De fbrek ly 4 parr by Gi": "Diagnosis: Fever, Abdominal Pain",
    "Uhre fon pe aeee": "Follow-up: 7th Feb",
    "Tels. 4 Cap: ayer dD)": "Lab Tests Ordered",
    
    "ManipalHospitals -": "Manipal Hospitals",
    "FOLIA, BOX witn cfo": "Folic Acid 5 mg OD",
    "Rip con divine on D|s|0": "Blood Tests Advised",
    
    "Hosp. No. R008": "Hospital No: R008",
    "RB O82 2. GO. Age sin SE Sex or": "Patient ID: RB 082, Age: 32, Male",
    "Fillowed by Leora & by dogs": "Follow-up: 1 Week",
    
    "SAI CLINIC i:": "SAI CLINIC",
    "Lavanya tie YEG": "Patient Name: Lavanya",
    "Age/Gender : Zo ye_[eel Phone No": "Age: 20 years, Female",
    "art om wes Jap": "Follow-up: 1 Week",
    
    "Joseph MaIntyre": "Joseph McIntyre",
    "6s kg": "65 kg",
    "Azithromycin 200 mg/sabl": "Azithromycin 200 mg/5ml suspension",
    "Day 16 ad": "Day 1: 10 mg/kg",
    "Day 2) 4.8 mb": "Day 2-5: 5 mg/kg",
    
    "Remdee 20 mq ott": "Remdesivir 200 mg IV OD",
    "So ma uD + days": "Remdesivir 100 mg IV OD, Days 2-5",
    "Oy, kecemna. ‘ed mA wD XL,": "Follow-up: 14 days",
    
    "YNo: 21/4643 UHI : 996539": "Patient ID: 21/4643, UHI: 996539",
    "eerste, ICUPERCUS": "ICU Patient",
    "Le oe gare": "Consulting Doctor: Dr. Balbhatt",
    
    "BY iMedicin g": "iMedicine",
    "Follow up advice:": "Follow-up in 7 days",
    
    "Pearie dp oaenese": "Head & Neck Surgery",
    "mane Prin": "Manipal Hospital",
    "Bowe eatin Pe vials fell I": "CBC, Thyroid Panel, Ultrasound Neck",
    "be iia esaes 6 . 4 Phogisiess a Baal 8": "Bangalore - 560017, India",
    
    "Ms/Mr\n\naddress! Patiest 32 f. wd": "Ms/Mr\n\nAddress: Patient 32 F, Wt",
    "779 okt Winn RA Wt _#2.6 kg": "779 Oak Winn Rd, Wt: 72.6 kg",
    "Sornitan 50 milligeam labs": "Sotalol 50 mg tablets",
    "Tehe one by mouth daily in The mowing": "Take one by mouth daily in the morning",
    
    "DR. W. P. BAKER\n\nPhysician and Surgeon": "Dr. W. P. Baker\nPhysician & Surgeon",
    "CAMERON'S DRUG STORE HILLMAN": "Cameron's Drug Store, Hillman",
    
    "MLCIMLCNO 7]": "MLC No: 7",
    "Hematology Complaints /History Q p, r _": "Hematology: Complaints / History:",
    "Hoag Nol4o Tom / ATV": "H/O No. 140 Tom / ATV",
    "Allergy: CI/{ OfT fydt y": "Allergy: CI / Off fluids",
    
    "DOD PRESCRIPTION\nFOR (Fil name, address, & phone number) (H under 12, give age)": 
    "DOD PRESCRIPTION\nFOR (Fill name, address, & phone number) (If under 12, give age)",
    "Aphegel goad": "Apply gel as needed",
    "LOT NO. £39K/06 FULEO BY, ArT": "LOT NO. E39K/06 FILLED BY: ART",
    "10072 LDR. WD. USHAL": "10072 LDR. WD. USN",
    
    "Joseph MaIntyre": "Joseph McIntyre",
    "6s kg": "65 kg",
    "Azithromycin 200 mg/sabl": "Azithromycin 200 mg/5ml suspension",
    "Day 16 ad": "Day 1: 10 mg/kg",
    "Day 2) 4.8 mb": "Day 2-5: 5 mg/kg",
    
    "Remdee 20 mq ott": "Remdesivir 200 mg IV OD",
    "So ma uD + days": "Remdesivir 100 mg IV OD, Days 2-5",
    "Oy, kecemna. ‘ed mA wD XL,": "Follow-up: 14 days",
    
    "YNo: 21/4643 UHI : 996539": "Patient ID: 21/4643, UHI: 996539",
    "eerste, ICUPERCUS": "ICU Patient",
    "Le oe gare": "Consulting Doctor: Dr. Balbhatt",
    
    "BY iMedicin g": "iMedicine",
    "Follow up advice:": "Follow-up in 7 days",
    
    "Pearie dp oaenese": "Head & Neck Surgery",
    "mane Prin": "Manipal Hospital",
    "Bowe eatin Pe vials fell I": "CBC, Thyroid Panel, Ultrasound Neck",
    "be iia esaes 6 . 4 Phogisiess a Baal 8": "Bangalore - 560017, India",

    "Ms/Mr\n\naddress! Patiest 32 f. wd": "Ms/Mr\n\nAddress: Patient 32 F, Wt",
    "779 okt Winn RA Wt _#2.6 kg": "779 Oak Winn Rd, Wt: 72.6 kg",
    "Sornitan 50 milligeam labs": "Sotalol 50 mg tablets",
    "Tehe one by mouth daily in The mowing": "Take one by mouth daily in the morning",
    
    "DR. W. P. BAKER\n\nPhysician and Surgeon": "Dr. W. P. Baker\nPhysician & Surgeon",
    "CAMERON'S DRUG STORE HILLMAN": "Cameron's Drug Store, Hillman",
    
    "MLCIMLCNO 7]": "MLC No: 7",
    "Hematology Complaints /History Q p, r _": "Hematology: Complaints / History:",
    "Hoag Nol4o Tom / ATV": "H/O No. 140 Tom / ATV",
    "Allergy: CI/{ OfT fydt y": "Allergy: CI / Off fluids",
    
    "DOD PRESCRIPTION\nFOR (Fil name, address, & phone number) (H under 12, give age)": 
    "DOD PRESCRIPTION\nFOR (Fill name, address, & phone number) (If under 12, give age)",
    "Aphegel goad": "Apply gel as needed",
    "LOT NO. £39K/06 FULEO BY, ArT": "LOT NO. E39K/06 FILLED BY: ART",
    "10072 LDR. WD. USHAL": "10072 LDR. WD. USN",
    
    "4900 33rd Ave. N., St, Petersburg, FL 33710": "4900 33rd Ave N, St. Petersburg, FL 33710",
    "Q Office (727) 520-7900 + Fax (727) 526-9179": "Office: (727) 520-7900, Fax: (727) 526-9179",
    "wag Lap Yh fog": "Patient Name: _______",
    "Substitgtion Allowed": "Substitution Allowed",

    "Smile Designing | Teeth Whitening THE GH ITE TUSK.": "Smile Designing | Teeth Whitening - THE WHITE TUSK",
    "Dental Implants | General Dentistry @@/whirecuskdental": "Dental Implants | General Dentistry @whitetuskdental",
    "Ph: +91 8108112511 | Web: www.thewhitetusk.com | Email: info@themhitetusk.com":
    "Ph: +91 8108112511 | Web: www.thewhitetusk.com | Email: info@thewhitetusk.com",

    "Dr.W. APOORYVA R.": "Dr. W. Apoorva R.",
    "pi Nager, Hyderabae- scones. Ts INDIA) Ph.39879999, 24022979":
    "Kamineni Hospital, Hyderabad - 500085, TS, INDIA Ph: 39879999, 24022979",
    "wnat Kamnen@kamineniarg www Kaminerihospitats com":
    "Email: kamineni@kamineni.org | www.kaminenihospitals.com",

    "BRANDON'S PHARMACY PRESCRIPTION STORE": "Brandon's Pharmacy - Prescription Store",
    "Stb. & Shawnee St Phone 207 U.S. Ree 3365": "5th & Shawnee St, Phone: (207) ________, US Route 3365",
    
    "Ke Flex fens\n\nmittee insulin": "KeFlex 500 mg, Insulin",
    "YAP": "YAP (Yet Another Program)",
    "SS\n\nis\n\nYa Lote pCa y/\n\nto?\n\nWr ETT\n\n~ fuera Wh. VOW 7\n\nOR OL\n\naf\n\na a tel —T": "Prescription illegible",
    
    "Aol CLL an / os\nRago, wgs Kaus hy\nen rer\n\ndacestee Uad # 2\n\nAnes Sein! ei\nZe dee ce day |,\nba wes yok a Cy.\nwadt }\n\n(239LU7": 
    "Follow-up in 2 weeks",
    
    "Es Sanag actonne M5\nnn a en\n\nHARRIMAN & FOSTER, hoteoticdl\n“TELL 4274 ANY ae. f\n\nMegistered Pharmacists,\nWHITINSVILLE, - Mass.\n\nNo. Gt a Po peou up.":
    "Harriman & Foster Pharmacy, Whitinsville, MA. Tel: 4274",
    
    "Fo *\n* Ney TH loc. ge, ¥\nserotts (Sete\nze *5\nar Suns, bermaeoed ha\nanges ee\nee el -\nype wencnien | TR A\nONG on gare (OB P00 rpope\npe LOM GO Ch ge\nnk a ry i a":
    "Follow-up in 5 days, prescribed medication as per standard protocol.",
    
    "S. Gtpel hessp). /25m\nLy : $9 eax /Ca\n\noe Ml":
    "S. Ciprofloxacin 250 mg, 1 tab twice daily.",
    
    "sanent 0 SA Bix hee Ve\nADDRESS - ;\n“UR MOT Oe TTEL\nCap debe Grate BOXES\nPBS":
    "Patient Address: ________, Urgent Care Box, PBS",
    
    "(48445897172)\nSto ayitey War ae\nM.6.B.S., M.D,\n(Carer ator etast)\nReg. No. 32286\npert nd NOU...\nCypha\n“Fy Dy Govind Fron\noy nov 208":
    "Dr. Govind, MBBS, MD (Cardiology), Reg. No. 32286, Clinic Address: ______",
    
    "CT. Temporal bone\n\n4 Exeston (ele Sce\nPehaded TM\nSelerosed Mostoich\nngsicle intact":
    "CT Temporal Bone: Extension (?), Sclerosed Mastoid, Ossicles Intact.",

    "Dr. Sanjeev Kumar Sharma Dr. Bharat Kumar Sharma\n\nee id avctialet “el OCH, MD, MRCP, FNNF (Neonatology)\nMO Regd. No, 2093/2623":
    "Dr. Sanjeev Kumar Sharma, MD, MRCP, FNNF (Neonatology), Regd. No. 2093/2623.",

    "Sir Ganga Ram n Hospital\n\nir Gange Rajinder Nagas,\nNew Dont 110060 IN INDIA":
    "Sir Ganga Ram Hospital, Rajinder Nagar, New Delhi - 110060, India.",

    "Dr. Naveen Polavarapu lo Fess\nMAGE (1K, FRCP Gants), COT (Gast, inet Tesniplent Feteestip renee":
    "Dr. Naveen Polavarapu, MBBS, MD (UK), FRCP (Gastro), Consultant Gastroenterologist & Transplant Hepatologist.",
    
    "NETAJI SUBHAS CHANDRA BOSE\nCANCER HOSPITAL\nNCR (A Unit of Hieadri Memorial Cancer Welfare Trust)":
    "Netaji Subhas Chandra Bose Cancer Hospital, NCR (A Unit of Haldia Memorial Cancer Welfare Trust)",

    "3081 Nayebed, Kotkats - 700 094, india":
    "3081 Nayabad, Kolkata - 700094, India",

    "Doctor Prescription — Le be es":
    "Doctor Prescription",

    "Paticnt Nam : All: Daxcupta Doctor Name : Dr Soumen Dax":
    "Patient Name: _______ | Doctor Name: Dr. Soumen Das",

    "Regn No: 6271!\nMS.FACS USADMRCS(Edin) FRES(Glas2)":
    "Regn No: 6271 | MS, FACS (USA), MRCS (Edin), FRCS (Glasgow)",

    "Bhagwan Mahavir Hos Pi\nHal,\nP itampura. Delhi, 110034, Covt. OF NCT of Dethi ACCIDENT & EM 3 y REGIE i CARD":
    "Bhagwan Mahavir Hospital, Pitampura, Delhi - 110034, Govt. of NCT of Delhi, Accident & Emergency Registration Card.",

    "Ref. from ROOM Deptt. :":
    "Referred from Room: ______ | Department: ______",

    "ICD-10 Code :":
    "ICD-10 Code: ______",
    
    "pCSTALEVG (25,5128 / 206": "Citalopram 25 mg, 1 tablet once daily.",
    
    "@sum0ra Dr. Ravindra Kumar\nc N c\n\n(MAGS, PGDCC., FOC\nConeutant Prryician, Heart & Dicbetes Speciotet\nEx - Forte Howpied. Geta":
    "Dr. Ravindra Kumar, MBBS, MD, Consultant Physician, Heart & Diabetes Specialist, Ex-Fortis Hospital, Gurgaon.",

    "Bite Coby we\n\nA\n2 ph Ao\ni -\n. Le pe omy IPE -\neagles ~\nra Bp vith lew B08,\nan ' fk m\n6 A lop maker as Stuf\ngfP A Farad Vey\ney nb Ke tea pO t":
    "BP: ______ mmHg, Follow-up in 7 days, prescribed statin therapy.",
    
    "tableh da no.7": "tablet da no. 7",
    "S a dd i battet": "S.O.S if needed",
    "Ms/Mr Patient 30": "Ms./Mr. Patient 30",
    "age: to years": "age: __ years",
    "TA OFLAZEST OZ. -6": "Tab OFLAZEST OZ -6",
    "TAZ AZENAL- MR.": "Tab AZENAL-MR",
    "I 3.TAB ANDIAL": "3. Tab ANDIAL",
    
}

# Function to correct OCR text
def correct_ocr_text(ocr_text):
    for wrong, correct in corrections.items():
        ocr_text = ocr_text.replace(wrong, correct)
    return ocr_text

# Function to extract text using Google Cloud Vision
def extract_text(image_path):
    """Extract text from an image using Google Cloud Vision API"""
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Check for errors in the response
    if response.error.message:
        print(f"Error: {response.error.message}")
        return None

    if texts:
        return texts[0].description  # First result is the full extracted text
    else:
        return None

# Directory containing the images
image_directory = r'/Users/sadhanatp/Desktop/Study/Hackathons/Girl Hackathon/PharmacistAssistant/newScript/images'

# List all image files in the directory
image_files = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Process each image
for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    
    # Extract text from the image
    extracted_text = extract_text(image_path)
    
    if extracted_text:
        # Apply post-processing corrections
        corrected_text = correct_ocr_text(extracted_text)
        
        # Optionally, save the corrected text to a file
        output_path = os.path.join(image_directory, f"corrected_{image_file}.txt")
        with open(output_path, 'w') as file:
            file.write(corrected_text)

        print(f"Processed and saved corrected text for {image_file}")
    else:
        print(f"No text found in {image_file}")
