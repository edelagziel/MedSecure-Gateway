import hashlib  # Import the hashlib library for checksum calculation

def verify_checksum(file, expected_checksum: str):
    # Verify that an expected checksum is provided
    if expected_checksum is None:
        raise ValueError("Missing checksum header")

    # Read the contents of the uploaded file
    file_content = file.file.read()

    # Calculate the actual checksum of the file content using SHA-256
    actual_checksum = hashlib.sha256(file_content).hexdigest()

    # Reset the file pointer back to the beginning
    file.file.seek(0)

    # Compare the actual checksum with the expected checksum (case-insensitive)
    if actual_checksum.lower() != expected_checksum.lower():
        raise ValueError("Checksum mismatch — file may be corrupted or tampered with")

    # Return True if the checksums match
    return True
