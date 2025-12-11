from fastapi import HTTPException  # Import HTTPException for error handling

def validate_file_size(file, max_size_bytes: int):
    """
    Validates that the uploaded file does not exceed the allowed size.
    Raises HTTPException(400) if too large.
    """
    # Move pointer to end of the file to determine its size
    file.file.seek(0, 2)  # Go to the end of the file
    size = file.file.tell()  # Get the current position, which is the file size

    # Reset file pointer back to the start so that subsequent reads are unaffected
    file.file.seek(0)

    # If the file size exceeds the maximum allowed size, raise a 400 HTTP error
    if size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size} bytes (max allowed: {max_size_bytes} bytes)"
        )
