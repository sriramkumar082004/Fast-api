import pytesseract
from PIL import Image
import io
import re
import os
import sys

# Set Tesseract Path explicitly for Windows
# This is needed because Tesseract is often not in the system PATH
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an image byte stream using Tesseract OCR.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")


def parse_aadhaar_details(text: str) -> dict:
    """
    Parses Aadhaar card details (Name, DOB, Gender, Aadhaar Number) from the extracted text.
    """
    details = {"name": None, "dob": None, "gender": None, "aadhaar_number": None}

    # Regex patterns
    # Aadhaar Number: 4 digits space 4 digits space 4 digits (e.g., 1234 5678 9012)
    aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"

    # Date of Birth: dd/mm/yyyy or dd-mm-yyyy
    dob_pattern = r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b"

    # Gender: Male, Female, or Transgender (Case insensitive)
    gender_pattern = r"\b(Male|Female|Transgender)\b"

    # Name: This is Tricky in OCR.
    # Strategy: Look for lines that look like a name (capitalized words) closer to the top
    # or often appearing before DOB/Aadhaar number.
    # For now, we will try to find a line that doesn't match other patterns and looks like a name.
    # This is a heuristic and might need refinement.

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Extract Aadhaar Number
    aadhaar_match = re.search(aadhaar_pattern, text)
    if aadhaar_match:
        details["aadhaar_number"] = aadhaar_match.group(0)

    # Extract DOB
    dob_match = re.search(dob_pattern, text)
    if dob_match:
        details["dob"] = dob_match.group(0).replace("-", "/")  # Standardize to /

    # Extract Gender
    gender_match = re.search(gender_pattern, text, re.IGNORECASE)
    if gender_match:
        details["gender"] = gender_match.group(0).title()

    # Extract Name (Heuristic)
    # Often, the info is in order: Name -> DOB -> Gender -> Aadhaar No.
    # We'll skip lines that contain keywords like "Government", "India", "DOB", "Year", "Male", "Female"
    skip_keywords = [
        "government",
        "india",
        "unique",
        "identification",
        "authority",
        "dob",
        "year",
        "male",
        "female",
        "father",
        "address",
        "help",
        "www",
        "enrolment",
    ]

    for line in lines:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in skip_keywords):
            continue

        # If line matches DOB or Aadhaar, skip
        if re.search(dob_pattern, line) or re.search(aadhaar_pattern, line):
            continue

        # If it's a short line or contains digits (names usually don't have digits, unless OCR error), verify
        if len(line) < 3 or any(char.isdigit() for char in line):
            # Allow some leniency for noise but typically names are pure letters
            # Let's filter slightly strictly for now
            continue

        # If we reached here, it's a candidate for Name.
        # Usually Name is the first significant line extracted that isn't excluded.
        if not details["name"]:
            details["name"] = line
            break

    return details
