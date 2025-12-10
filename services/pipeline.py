from .checksum import verify_checksum
from .quarantine import move_to_quarantine
from .mime_validation import validate_mime_type
from .validate_metadata import validate_metadata
from fastapi import HTTPException



allowed_types = [
    "application/pdf",
    "text/plain",
    "text/csv",
    "application/json"
]

allowed_extensions = ["pdf", "txt", "csv", "json"]


def process_file(file, checksum):
    try:
        verify_checksum(file,checksum)
        validate_mime_type(file,file.content_type,allowed_types)
        validate_metadata(file,allowed_extensions)
        return {"received": True, "filename": file.filename, "checksum": checksum}
    except Exception as e:
        move_to_quarantine(file)
        raise HTTPException(status_code=400, detail=str(e))




