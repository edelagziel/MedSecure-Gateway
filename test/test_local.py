from services.validate_size import validate_file_size
from services.staging import stage_file_temporarily
from services.quarantine import move_to_quarantine
from services.email_alerts import send_security_alert
from virus_scanning.av_scanner import scan_file, ScanStatus

from fastapi import UploadFile
from io import BytesIO


# Helper: create UploadFile object from raw bytes
def make_upload_file(content: bytes, filename="test.txt"):
    return UploadFile(filename=filename, file=BytesIO(content))


print("\n=== TEST 1: File Size Validation ===")
small_file = make_upload_file(b"hello world")
validate_file_size(small_file, max_size_bytes=1024)  # should pass
print("✔ Small file passed size validation")

try:
    big_file = make_upload_file(b"x" * 2_000_000)  # ~2MB
    validate_file_size(big_file, max_size_bytes=1_000_000)
except Exception as e:
    print("✔ Large file correctly failed:", e)


print("\n=== TEST 2: Temporary Staging ===")
staged_path = stage_file_temporarily(small_file)
print("✔ Temp file created at:", staged_path)


print("\n=== TEST 3: AV Scanner (expected ERROR, since ClamAV not running) ===")
result = scan_file(staged_path)
print("✔ AV scan result:", result.status, result.signature)


print("\n=== TEST 4: Move to Quarantine ===")
quarantine_path = move_to_quarantine(small_file)
print("✔ File moved to quarantine:", quarantine_path)


print("\n=== TEST 5: Security Alert ===")
alert = send_security_alert("test.txt", "manual test")
print("✔ Alert generated:", alert)
