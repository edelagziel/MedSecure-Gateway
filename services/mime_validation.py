import magic  # Import the python-magic library for MIME type detection

def validate_mime_type(file, declared_type, allowed_types):
    sample = file.file.read(2048)  # Read the first 2048 bytes from the uploaded file
    file.file.seek(0)  # Reset the file pointer back to the beginning

    detected_type = magic.from_buffer(sample, mime=True)  # Detect MIME type from the sample buffer

    if declared_type != detected_type:  # Check for mismatch between declared and detected MIME types
        raise ValueError(
            f"MIME mismatch: declared={declared_type}, detected={detected_type}"
        )

    if detected_type not in allowed_types:  # Check if the detected MIME type is allowed
        raise ValueError(f"Unsupported MIME type: {detected_type}")

    return detected_type  # Return the detected MIME type
