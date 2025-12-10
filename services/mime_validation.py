import magic

def validate_mime_type(file, declared_type, allowed_types):
    sample = file.file.read(2048)
    file.file.seek(0)

    detected_type = magic.from_buffer(sample, mime=True)

    if declared_type != detected_type:
        raise ValueError(
            f"MIME mismatch: declared={declared_type}, detected={detected_type}"
        )

    if detected_type not in allowed_types:
        raise ValueError(f"Unsupported MIME type: {detected_type}")

    return detected_type
