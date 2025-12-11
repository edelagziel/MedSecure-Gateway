from .checksum import verify_checksum                 # Import checksum verification function
from .quarantine import move_to_quarantine           # Import function to move files to quarantine
from .mime_validation import validate_mime_type      # Import MIME type validation function
from .validate_metadata import validate_metadata     # Import metadata validation function

from .validate_size import validate_file_size        # Import file size validation function
from services.email_alerts import send_security_alert # Import security alert email function

from .save_uploadfile import save_file_permanently   # Import function to save uploaded files permanently
from fastapi import HTTPException                    # Import HTTPException from FastAPI
from .AV_scanner import scan_file                    # Import antivirus scan function
from services.s3_upload import upload_to_s3          # Import S3 upload function



allowed_types = [
    "application/pdf",                               # Allow PDF files
    "text/plain",                                    # Allow plain text files
    "text/csv",                                      # Allow CSV files
    "application/json"                               # Allow JSON files
]

allowed_extensions = ["pdf", "txt", "csv", "json"]   # Allow only these file extensions

MAX_UPLOAD_SIZE = 10 * 1024 * 1024                   # Set maximum upload size to 10 MB

def process_file(file, checksum):
    file_location = save_file_permanently(file)      # Save uploaded file permanently and get its location
    try:
        verify_checksum(file,checksum)               # Verify file checksum
        validate_mime_type(file,file.content_type,allowed_types) # Validate MIME type of the file
        validate_metadata(file,allowed_extensions)   # Validate file metadata (including extension)
        validate_file_size(file,MAX_UPLOAD_SIZE)     # Check file size limits
        scan_file(file_location)                     # Scan the file for viruses or malware
        upload_to_s3(file_location, file.filename)   # Upload file to S3 storage
        return {"received": True, "filename": file.filename, "checksum": checksum} # Return success response

    except Exception as e:
        # Move file to quarantine folder
        move_to_quarantine(file_location, reason=str(e))

        # Send security alert
        send_security_alert(filename=file.filename,reason=str(e))

        raise HTTPException(status_code=400, detail=str(e)) # Raise HTTP error with appropriate details

