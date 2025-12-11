from fastapi import FastAPI  # Import FastAPI framework
from fastapi import UploadFile, File, Header  # Import classes to handle file uploads and headers
from services.pipeline import process_file  # Import the file processing function

app = FastAPI()  # Initialize the FastAPI app


@app.get("/health")
def health_check():
    # Health check endpoint to verify the server is running
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),  # Expect an uploaded file as form-data
    checksum: str = Header(None)   # Optionally receive a checksum in request headers
):
    # Pass the uploaded file and checksum to the processing pipeline
    result = process_file(file, checksum)
    return result  # Return the result from the pipeline
