def validate_metadata(file, allowed_extensions):
    # Retrieve the filename from the uploaded file
    filename = file.filename

    # Block path traversal by checking for directory components in filename
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename: path traversal detected")

    # List of forbidden characters in filenames
    forbidden_chars = ['\0', '<', '>', ':', '"', '|', '?', '*']
    # Check if any forbidden character is present in the filename
    if any(c in filename for c in forbidden_chars):
        raise ValueError("Invalid filename: contains forbidden characters")

    # Require that the filename has at least one "." indicating an extension
    if "." not in filename:
        raise ValueError("Missing file extension")

    # Extract the file extension and normalize to lowercase
    ext = filename.rsplit(".", 1)[-1].lower()

    # Validate the extension against the allowed list
    if ext not in allowed_extensions:
        raise ValueError(f"Unsupported extension: .{ext}")

    # If all checks pass, return True
    return True
