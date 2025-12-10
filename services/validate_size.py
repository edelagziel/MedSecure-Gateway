from fastapi import HTTPException

def validate_file_size(file, max_size_bytes: int):
    """
    Validates that the uploaded file does not exceed the allowed size.
    Raises HTTPException(400) if too large.
    """
    # Move pointer to end to determine size
    file.file.seek(0, 2)  # go to end
    size = file.file.tell()

    # Reset pointer back to start
    file.file.seek(0)

    if size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {size} bytes (max allowed: {max_size_bytes} bytes)"
        )
