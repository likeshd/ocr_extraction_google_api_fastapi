from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from api_functions import passport_ocr_extraction  # Import function from passport_ocr.py
from io import BytesIO
from PIL import Image

# Initialize FastAPI app
app = FastAPI()

# FastAPI route to handle the image upload and OCR extraction
@app.post("/extract_passport_details")
async def extract_passport_details(file: UploadFile):
    try:
        # Read image file
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        # Get OCR extraction result from the imported function
        result, status_code = await passport_ocr_extraction(image)

        # Return the result as a JSON response
        return JSONResponse(content=result, status_code=status_code)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)



# Testing the FastAPI app locally
if __name__ == "__main__":
    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)