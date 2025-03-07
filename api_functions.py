import base64
import json
import os
import requests
from io import BytesIO
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Securely retrieve API key from environment variable
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-2.0-flash') # Changed model

# Asynchronous OCR function using Google API
async def pass_ocr_extraction(image_input):

    image = image_input
    # Prepare the prompt for the Gemini Pro Vision model
    prompt = """Act as an OCR assistant.
                            If the provided image contains text that is not properly oriented, correct its orientation before extracting the text.  
                            If  provided image is not country passport then write its not country passport image.
                            Extract the following details from the provided image and return them in JSON format:
                            {
                                "Passport No": "",
                                "Surname": "",
                                "Given Names": "",
                                "Nationality": "",
                                "Country code": "",
                                "Date of Birth": "YYYY-MM-DD",
                                "Sex": "M/F",
                                "Place of Birth": "",
                                "Date of Issue": "YYYY-MM-DD",
                                "Issuing Authority or Place of Issue": "",
                                "Date of Expiry": "YYYY-MM-DD",
                                "Address": ""
                            }
                            If any field is missing or unclear, return it as `null`.
                            """


    # Make the Gemini Pro Vision API call
    response = model.generate_content([prompt, image])
    raw_content = response.text

    # Remove Markdown-style JSON formatting if present
    if raw_content.startswith("```json"):

        raw_content = raw_content.strip("```json").strip("```")
        # Parse the response as JSON
        parsed_data = json.loads(raw_content)
        # Convert to required format

        data = {
            "id": parsed_data.get("Passport No", ""),
            "givennames": parsed_data.get("Given Names", ""),
            "surname": parsed_data.get("Surname", ""),
            "dob": parsed_data.get("Date of Birth", ""),
            "code": parsed_data.get("Country code", ""),
            "issuedate": parsed_data.get("Date of Issue", ""),
            "expirydate": parsed_data.get("Date of Expiry", ""),
            "address": parsed_data.get("Address", ""),
            "sex": parsed_data.get("Sex", ""),
            "nationality": parsed_data.get("Nationality", ""),
            "placeofissue": parsed_data.get("Issuing Authority or Place of Issue", ""),
            "placeofbirth": parsed_data.get("Place of Birth", "")

        }
        print(data)
        return data, 200
    else:
        data = raw_content
        return data, 400

# Asynchronous OCR function using Google API
async def visa_ocr_extraction(image_input):

    image = image_input

    # Prepare the prompt for the Gemini Pro Vision model
    prompt = """Read the text from right to left where applicable.
                            If the provided image contains text that is not properly oriented, correct its orientation before extracting the text.
                            Extract the following details from the image and return them in JSON format:
                            {
                                "UID Number": "",
                                "File or Entry Permit No": "",
                                "Place of Issue": "",
                                "Passport No": "",
                                "Name": "",
                                "Profession": "",
                                "Sponsor": "",
                                "Accompanied_by": "",
                                "Date of Birth": "YYYY-MM-DD",
                                "Issue_Date": "YYYY-MM-DD",
                                "Expiry_Date": "YYYY-MM-DD"
                            }
                            If any parameter is missing or unclear, return it as `null`. 
                            """


    # Make the Gemini Pro Vision API call
    response = model.generate_content([prompt, image])
    raw_content = response.text

    # Remove Markdown-style JSON formatting if present
    if raw_content.startswith("```json"):

        raw_content = raw_content.strip("```json").strip("```")
        # Parse the response as JSON
        parsed_data = json.loads(raw_content)
        # Convert to required format

        data = {
                "id": parsed_data.get("File or Entry Permit No", ""),
                "name": parsed_data.get("Name", ""),
                "uid": parsed_data.get("UID Number", ""),
                "dob": parsed_data.get("Date of Birth", ""),
                "issuedate": parsed_data.get("Issue_Date", ""),
                "expirydate": parsed_data.get("Expiry_Date", ""),
                "profession": parsed_data.get("Profession", ""),
                "sponsor": parsed_data.get("Sponsor", ""),
                "passport_id": parsed_data.get("Passport No", ""),
                "placeofissue": parsed_data.get("Place of Issue", ""),

        }
        print(data)
        return data, 200
    else:
        data = raw_content
        return data, 400

# Asynchronous OCR function using Google API
async def eid_ocr_extraction(image_input):

    image = image_input

    # Prepare the prompt for the Gemini Pro Vision model
    prompt = """
                If the provided image contains text that is not properly oriented, correct its orientation before extracting the text.  
                Extract the following details from the image and return them in JSON format:
                    {
                        "ID_Number": "",
                        "Name": "",
                        "Date_of_Birth": "YYYY-MM-DD",
                        "Nationality": "",
                        "Issuing_Date": "YYYY-MM-DD",
                        "Expiry_Date": "YYYY-MM-DD",
                        "Occupation": "",
                        "Employer": "",
                        "Issuing_Place": ""
                    }
                    Ensure the extracted text is accurate. If a field is missing or unclear, return `null`.
                    """


    # Make the Gemini Pro Vision API call
    response = model.generate_content([prompt, image])
    raw_content = response.text

    # Remove Markdown-style JSON formatting if present
    if raw_content.startswith("```json"):

        raw_content = raw_content.strip("```json").strip("```")
        # Parse the response as JSON
        parsed_data = json.loads(raw_content)

        # Convert to required format
        data = {
                "id": parsed_data.get("ID_Number", ""),
                "name": parsed_data.get("Name", ""),
                "nationality": parsed_data.get("Nationality", ""),
                "dob": parsed_data.get("Date_of_Birth", ""),
                "issuedate": parsed_data.get("Issuing_Date", ""),
                "expirydate": parsed_data.get("Expiry_Date", ""),
                "occupation": parsed_data.get("Occupation", ""),
                "employer": parsed_data.get("Employer", ""),
                "placeofissue": parsed_data.get("Issuing_Place", "")

            }

        print(data)
        return data, 200
    else:
        data = raw_content
        return data, 400

# Asynchronous OCR function using Google API
async def dl_ocr_extraction(image_input):

    image = image_input

    # Prepare the prompt for the Gemini Pro Vision model
    prompt = """
                If the provided image contains text that is not properly oriented, correct its orientation before extracting the text.
                Extract the following details from the provided image and return them in structured JSON format:
                    {
                        "License No": "",
                        "Name": "",
                        "Nationality": "",
                        "Date_of_Birth": "YYYY-MM-DD",
                        "Issue_Date": "YYYY-MM-DD",
                        "Expiry_Date": "YYYY-MM-DD",
                        "Place_of_Issue": ""
                    }
                    Ensure high accuracy in data extraction.
                    If any parameter is missing or unclear, return `null` instead of guessing the value.
                    """


    # Make the Gemini Pro Vision API call
    response = model.generate_content([prompt, image])
    raw_content = response.text

    # Remove Markdown-style JSON formatting if present
    if raw_content.startswith("```json"):

        raw_content = raw_content.strip("```json").strip("```")
        # Parse the response as JSON
        parsed_data = json.loads(raw_content)

        # Convert to required format
        data = {
                "id": parsed_data.get("License No", ""),
                "name": parsed_data.get("Name", ""),
                "nationality": parsed_data.get("Nationality", ""),
                "dob": parsed_data.get("Date_of_Birth", ""),
                "issuedate": parsed_data.get("Issue_Date", ""),
                "expirydate": parsed_data.get("Expiry_Date", ""),
                "placeofissue": parsed_data.get("Place_of_Issue", "")

            }

        print(data)
        return data, 200
    else:
        data = raw_content
        return data, 400

# Testing the functions in passport_ocr.py
if __name__ == "__main__":
    # Example test case
    pass
    # image_path = "path_to_image.jpg"  # Replace with an actual image path
    # image = Image.open(image_path)
    #
    # # Run the asynchronous function to test OCR extraction
    # import asyncio
    # loop = asyncio.get_event_loop()
    # result, status_code = loop.run_until_complete(passport_ocr_extraction(image))
    #
    # print(f"Status Code: {status_code}")
    # print("OCR Result:", result)