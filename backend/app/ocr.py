import cv2
import pytesseract
import re
import numpy as np
import platform

# 1. Smart Path Selection (Works on both your Laptop and Render)
if platform.system() == "Windows":
    # On Windows, we expect Tesseract to be in the system PATH
    pass
else:
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def preprocess_image(image):
    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize (Upscale 2x) - Helps read small dates
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Adaptive Thresholding (Standard OTSU is often safer for text)
    # We use OTSU because aggressive adaptive thresholding can sometimes erase thin text
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return gray


def extract_aadhaar_data(image_bytes):
    # Convert bytes to image
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Failed to decode image"}

    processed_img = preprocess_image(image)

    # psm 6 = Assume a single uniform block of text
    text = pytesseract.image_to_string(processed_img, lang="eng", config="--psm 6")

    # Clean text: Remove empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # --- 1. Gender Extraction (Fuzzy Logic) ---
    # We use regex to catch "MALE", "MA1E", "FEMALE", "FEMA|E", etc.
    gender = "Unknown"
    text_upper = text.upper()

    # Check Female first (because "Female" contains the word "Male")
    if re.search(r"\b(FEMALE|FEMA1E|FEMALE|F\/F|FEM)\b", text_upper):
        gender = "Female"
    elif re.search(r"\b(MALE|MA1E|MAL|M\/M)\b", text_upper):
        gender = "Male"
    elif "TRANSGENDER" in text_upper:
        gender = "Transgender"

    # --- 2. DOB Extraction (Flexible) ---
    # Matches: 12/05/2000, 12-05-2000, 12.05.2000, 12 05 2000
    # Also handles common OCR errors like 'O' instead of '0'
    dob = None
    dob_line_index = -1

    # Regex looks for: 2 digits + separator + 2 digits + separator + 4 digits
    date_pattern = r"\b\d{2}[-/\.\s]\d{2}[-/\.\s]\d{4}\b"

    # Scan lines to find the specific line with the DOB
    for i, line in enumerate(lines):
        # Fix common OCR number errors just for checking
        line_fixed = line.replace("O", "0").replace("l", "1").replace("I", "1")
        match = re.search(date_pattern, line_fixed)
        if match:
            dob = match.group(0).replace(" ", "/")  # Standardize format
            dob_line_index = i
            break

    # Fallback: If loop didn't find it, search whole text
    if not dob:
        match = re.search(date_pattern, text.replace("O", "0"))
        if match:
            dob = match.group(0)

    # --- 3. Name Extraction (Context Aware) ---
    name = None

    # Strategy A: Look ABOVE the DOB line (Standard format)
    if dob_line_index > 0:
        # Check 1 line above
        candidate = lines[dob_line_index - 1]

        # If line is junk (Header or Gender), check 2 lines above
        junk_words = [
            "DOB",
            "YEAR",
            "BIRTH",
            "GOVERNMENT",
            "INDIA",
            "MALE",
            "FEMALE",
            "ADDRESS",
        ]
        if any(word in candidate.upper() for word in junk_words) or len(candidate) < 4:
            if dob_line_index > 1:
                candidate = lines[dob_line_index - 2]

        # Verify it looks like a name (mostly letters, no numbers)
        if is_valid_name(candidate):
            name = candidate

    # Strategy B: Fallback (If Strategy A failed)
    # Take the first line that looks like a name and isn't a header
    if not name:
        for line in lines[:5]:  # Only check top 5 lines
            if is_valid_name(line):
                name = line
                break

    return {
        "aadhaar_number": extract_aadhaar_number(text),  # Helper function below
        "dob": dob,
        "gender": gender,
        "name": name,
        "raw_text": text,  # Helpful for debugging
    }


def extract_aadhaar_number(text):
    # Matches 12 digits with optional spaces: 1234 5678 9012
    match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)
    return match.group(0) if match else None


def is_valid_name(text):
    # Helper to check if a line is likely a name
    bad_words = ["GOVT", "INDIA", "ADHAAR", "DOB", "YEAR", "FATHER", "ADDRESS"]
    if any(w in text.upper() for w in bad_words):
        return False
    # Must be at least 3 chars and mostly letters
    if len(text) < 3:
        return False
    # If it contains digits (like an address 12/4), it's not a name
    if re.search(r"\d", text):
        return False
    return True
