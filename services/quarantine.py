
from datetime import datetime  # Import datetime module for working with timestamps (not used here)
from pathlib import Path      # Import Path for handling filesystem paths
import shutil                 # Import shutil for file operations

# קביעת נתיב לתיקיית הסגר
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Set project root as parent directory of current file
QUARANTINE_DIR = PROJECT_ROOT / "quarantine"           # Define quarantine directory path
QUARANTINE_DIR.mkdir(exist_ok=True)                    # Create the quarantine directory if it does not exist

def move_to_quarantine(file_path, reason="unspecified"):
    file_name = Path(file_path).name                   # Extract file name from the file path
    quarantine_target = QUARANTINE_DIR / file_name     # Set the destination path within the quarantine directory

    shutil.move(file_path, quarantine_target)          # Move the file to the quarantine directory

    log_file = quarantine_target.with_suffix(".log")   # Create a log file alongside the quarantined file
    with open(log_file, "w") as log:                   # Open the log file for writing
        log.write(f"File: {file_name}\n")              # Write the file name to the log
        log.write(f"Reason: {reason}\n")               # Write the quarantine reason to the log

    print(f"[QUARANTINE] File moved to {quarantine_target} (Reason: {reason})")  # Print status

    return str(quarantine_target)                      # Return the path of the quarantined file as a string

