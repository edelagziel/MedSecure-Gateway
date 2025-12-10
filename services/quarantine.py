import os
import shutil
from datetime import datetime
from pathlib import Path

QUARANTINE_DIR = Path("quarantine")


def move_to_quarantine(file):
    """
    Saves the uploaded file into the local quarantine folder.
    Creates a timestamped filename to avoid collisions.
    """

    # Ensure quarantine directory exists
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    # Extract original filename
    original_name = file.filename or "unnamed_file"

    # Generate timestamped name
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    quarantined_name = f"{timestamp}_{original_name}"

    # Full path to save the quarantined file
    quarantined_path = QUARANTINE_DIR / quarantined_name

    # Save the file content
    file.file.seek(0)  # make sure pointer at start
    with open(quarantined_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    print(f"[QUARANTINE] Stored file at: {quarantined_path}")

    return str(quarantined_path)
