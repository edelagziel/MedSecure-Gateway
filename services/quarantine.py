
from datetime import datetime
from pathlib import Path
import shutil

# קביעת נתיב לתיקיית הסגר
PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUARANTINE_DIR = PROJECT_ROOT / "quarantine"
QUARANTINE_DIR.mkdir(exist_ok=True)

def move_to_quarantine(file_path, reason="unspecified"):
    file_name = Path(file_path).name
    quarantine_target = QUARANTINE_DIR / file_name

    shutil.move(file_path, quarantine_target)

    log_file = quarantine_target.with_suffix(".log")
    with open(log_file, "w") as log:
        log.write(f"File: {file_name}\n")
        log.write(f"Reason: {reason}\n")

    print(f"[QUARANTINE] File moved to {quarantine_target} (Reason: {reason})")

    return str(quarantine_target)





# from datetime import datetime
# from pathlib import Path
# import shutil

# # PROJECT_ROOT = MedSecure-Gateway/
# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# # Always use the quarantine folder in the project root:
# QUARANTINE_DIR = PROJECT_ROOT / "quarantine"


# def move_to_quarantine(file, reason: str = "unspecified"):
#     """
#     Saves the uploaded file into the local quarantine folder in the project root.
#     Creates a timestamped filename to avoid collisions.
#     Optionally records the reason for quarantine.
#     """

#     # Ensure quarantine directory exists
#     QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

#     # Original filename (or fallback)
#     original_name = file.filename or "unnamed_file"

#     # Generate timestamped filename
#     timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
#     quarantined_name = f"{timestamp}_{original_name}"

#     # Full file path
#     quarantined_path = QUARANTINE_DIR / quarantined_name

#     # Save file contents
#     file.file.seek(0)  # make sure we start from the beginning
#     with open(quarantined_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Optional: simple text log next to the quarantined file
#     log_path = QUARANTINE_DIR / f"{timestamp}_{original_name}.log"
#     with open(log_path, "w", encoding="utf-8") as log:
#         log.write(f"File: {original_name}\n")
#         log.write(f"Stored: {timestamp} UTC\n")
#         log.write(f"Reason: {reason}\n")

#     print(f"[QUARANTINE] Stored file at: {quarantined_path} (Reason: {reason})")

#     return str(quarantined_path)
