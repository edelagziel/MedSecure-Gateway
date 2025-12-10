def validate_metadata(file, allowed_extensions):
    filename = file.filename

    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename: path traversal detected")

    forbidden_chars = ['\0', '<', '>', ':', '"', '|', '?', '*']
    if any(c in filename for c in forbidden_chars):
        raise ValueError("Invalid filename: contains forbidden characters")

    if "." not in filename:
        raise ValueError("Missing file extension")

    ext = filename.rsplit(".", 1)[-1].lower()

    if ext not in allowed_extensions:
        raise ValueError(f"Unsupported extension: .{ext}")

    return True
