from pathlib import Path  # Import Path for handling filesystem paths
import shutil  # Import shutil for file copying

# Create the "incoming" directory (in the parent directory of the current file) if it doesn't exist
INCOMING_DIR = Path(__file__).resolve().parent.parent / "incoming"
INCOMING_DIR.mkdir(exist_ok=True)


def save_file_permanently(upload_file):
    """
    Saves UploadFile as a permanent file in /incoming and returns the file path.
    """
    filename = upload_file.filename or "unnamed_file"  # Use the original filename or a default
    dest = INCOMING_DIR / filename  # Determine destination path in the incoming folder

    # Copy file content from uploaded file object to the permanent file on disk
    upload_file.file.seek(0)  # Ensure pointer is at start before copying
    with open(dest, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)  # Copy the file data

    # After saving, reset the file pointer to the start for any further reads
    upload_file.file.seek(0)

    return str(dest)  # Return the resulting file path as a string

