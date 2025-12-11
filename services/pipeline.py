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

# from fastapi import HTTPException
#
# from services.validate_size import validate_file_size
# from services.mime_validation import validate_mime_type
# from services.validate_metadata import validate_metadata
# from services.checksum import verify_checksum
# from services.quarantine import move_to_quarantine
# from services.email_alerts import send_security_alert
# from services.save_uploadfile import save_file_permanently
# from services.AV_scanner import scan_file
# from services.s3_upload import upload_to_s3  # ⬅️ החדש!
#
# import os
#
#
# # Allowed MIME types & extensions
# allowed_types = [
#     "application/pdf",
#     "text/plain",
#     "text/csv",
#     "application/json"
# ]
#
# allowed_extensions = ["pdf", "txt", "csv", "json"]
#
# MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
#
#
# def process_file(file, checksum):
#     """
#     Secure file-processing pipeline:
#
#     1. Validate size
#     2. Validate MIME type
#     3. Validate metadata
#     4. Save file permanently to /incoming
#     5. Antivirus scan
#     6. Verify checksum
#     7. Upload clean file to S3
#     8. On failure → quarantine + alert + HTTP 400
#     """
#
#     try:
#         # 1. Validate file size
#         validate_file_size(file, MAX_UPLOAD_SIZE)
#
#         # 2. Validate MIME type
#         validate_mime_type(file, file.content_type, allowed_types)
#
#         # 3. Validate metadata (filename / extension)
#         validate_metadata(file, allowed_extensions)
#
#         # 4. Save file permanently
#         file_location = save_file_permanently(file)
#
#         # 5. Antivirus scan
#         scan_file(file_location)  # raises ValueError on infected/error
#
#         # 6. Verify checksum AFTER AV & validations
#         verify_checksum(file, checksum)
#
#         # 7. Upload clean file to S3
#         upload_to_s3(file_location, file.filename)
#
#         # SUCCESS RESPONSE
#         return {
#             "received": True,
#             "filename": file.filename,
#             "checksum": checksum,
#             "uploaded_to_s3": True
#         }
#
#     except Exception as e:
#         reason = str(e)
#
#         # Attempt to quarantine only if file was saved
#         try:
#             if "file_location" in locals():
#                 move_to_quarantine(file_location, reason=reason)
#         except:
#             pass  # quarantine failed silently — acceptable in assignment
#
#         # Send alert email (printed to console)
#         send_security_alert(filename=file.filename, reason=reason)
#
#         # Return HTTP error to client
#         raise HTTPException(status_code=400, detail=reason)