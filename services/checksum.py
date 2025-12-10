import hashlib

def verify_checksum(file, expected_checksum: str):
  

    if expected_checksum is None:
        raise ValueError("Missing checksum header")

    file_content = file.file.read()

    actual_checksum = hashlib.sha256(file_content).hexdigest()

    file.file.seek(0)

    if actual_checksum.lower() != expected_checksum.lower():
        raise ValueError("Checksum mismatch — file may be corrupted or tampered with")

    return True
