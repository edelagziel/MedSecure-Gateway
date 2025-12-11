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
#
# from virus_scanning.av_scanner import scan_file, ScanStatus
#
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
# MAX_UPLOAD_SIZE = 10 * 1024 * 1024
#
#
# def process_file(file, checksum):
#
#     try:
#         # 1. Size check
#         validate_file_size(file, MAX_UPLOAD_SIZE)
#
#         # 2. MIME
#         validate_mime_type(file, file.content_type, allowed_types)
#
#         # 3. Metadata
#         validate_metadata(file, allowed_extensions)
#
#         # 4. Temporary staging
#         temp_path = stage_file_temporarily(file)
#
#         # 5. AV scan on the staged file
#         av_result = scan_file(temp_path)
#
#         if av_result.status == ScanStatus.INFECTED:
#             raise ValueError(f"AV blocked file: {av_result.signature}")
#
#         if av_result.status == ScanStatus.ERROR:
#             raise ValueError(f"AV scan error: {av_result.signature}")
#
#         # 6. Checksum validation (only after file is considered clean)
#         verify_checksum(file, checksum)
#
#         return {"received": True, "filename": file.filename, "checksum": checksum}
#
#     except Exception as e:
#         # quarantine original uploaded file
#         move_to_quarantine(file, reason=str(e))
#
#         # send alert
#         send_security_alert(file.filename, reason=str(e))
#
#         raise HTTPException(status_code=400, detail=str(e))


