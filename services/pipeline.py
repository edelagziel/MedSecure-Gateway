from .checksum import verify_checksum
from .quarantine import move_to_quarantine
from .mime_validation import validate_mime_type
from .validate_metadata import validate_metadata

from .validate_size import validate_file_size
from services.email_alerts import send_security_alert

from .save_uploadfile import save_file_permanently
from fastapi import HTTPException
from .AV_scanner import scan_file
from services.s3_upload import upload_to_s3



allowed_types = [
    "application/pdf",
    "text/plain",
    "text/csv",
    "application/json"
]

allowed_extensions = ["pdf", "txt", "csv", "json"]

MAX_UPLOAD_SIZE = 10 * 1024 * 1024

def process_file(file, checksum):
    file_location = save_file_permanently(file)
    try:
        verify_checksum(file,checksum)
        validate_mime_type(file,file.content_type,allowed_types)
        validate_metadata(file,allowed_extensions)
        validate_file_size(file,MAX_UPLOAD_SIZE)
        scan_file(file_location)
        upload_to_s3(file_location, file.filename)
        return {"received": True, "filename": file.filename, "checksum": checksum}

    except Exception as e:
        # Move file to quarantine folder
        move_to_quarantine(file_location, reason=str(e))

        # Send security alert
        send_security_alert(filename=file.filename,reason=str(e))

        raise HTTPException(status_code=400, detail=str(e))

