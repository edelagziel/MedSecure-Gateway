from .checksum import verify_checksum
from .quarantine import move_to_quarantine
from .mime_validation import validate_mime_type
from .validate_metadata import validate_metadata

from .validate_size import validate_file_size
from services.email_alerts import send_security_alert

from .save_uploadfile import save_file_permanently
from fastapi import HTTPException
from .AV_scanner import scan_file


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
        return {"received": True, "filename": file.filename, "checksum": checksum}
    
    except Exception as e:
        # Move file to quarantine folder
        move_to_quarantine(file_location, reason=str(e))

        # Send security alert
        send_security_alert(filename=file.filename,reason=str(e))

        raise HTTPException(status_code=400, detail=str(e))


# from fastapi import HTTPException
#
# from .validate_size import validate_file_size
# from .mime_validation import validate_mime_type
# from .validate_metadata import validate_metadata
# from .staging import stage_file_temporarily
# from .checksum import verify_checksum
# from .quarantine import move_to_quarantine
# from alerts.email_alerts import send_security_alert
# from AV_scanner import scan_file   # התאימי למיקום הנכון אצלך
#
# allowed_types = [
#     "application/pdf",
#     "text/plain",
#     "text/csv",
#     "application/json"
# ]
#
# allowed_extensions = ["pdf", "txt", "csv", "json"]
#
# MAX_UPLOAD_SIZE = 10 * 1024 * 1024   # 10MB
#
#
# def process_file(file, checksum):
#     """
#     Complete secure upload pipeline:
#     - Validations (size, MIME, metadata)
#     - Temporary staging
#     - AV scanning
#     - Checksum validation
#     - Quarantine + alerting on failure
#     """
#
#     try:
#         # 1. Validate file size
#         validate_file_size(file, MAX_UPLOAD_SIZE)
#
#         # 2. Validate MIME type
#         validate_mime_type(file, file.content_type, allowed_types)
#
#         # 3. Validate filename extension metadata
#         validate_metadata(file, allowed_extensions)
#
#         # 4. Stage file temporarily (required by assignment)
#         temp_path = stage_file_temporarily(file)
#
#         # 5. Antivirus scan on the staged file
#         scan_file(temp_path)  # raises ValueError on infected/error
#
#         # 6. Verify integrity only after file passes all previous tests
#         verify_checksum(file, checksum)
#
#         # SUCCESS
#         return {
#             "received": True,
#             "filename": file.filename,
#             "checksum": checksum
#         }
#
#     except Exception as e:
#
#         # Quarantine the staged file (path)
#         try:
#             move_to_quarantine(temp_path, reason=str(e))
#         except:
#             pass  # אם staging itself נכשל, אין מה לבודד
#
#         # Generate a security alert
#         send_security_alert(
#             filename=file.filename,
#             reason=str(e)
#         )
#
#         # Final error to the user
#         raise HTTPException(status_code=400, detail=str(e))

