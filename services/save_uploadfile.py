from pathlib import Path
import shutil

# תיקיית קבצים נכנסים
INCOMING_DIR = Path(__file__).resolve().parent.parent / "incoming"
INCOMING_DIR.mkdir(exist_ok=True)


def save_file_permanently(upload_file):
    """
    Saves UploadFile as a permanent file in /incoming and returns the file path.
    """
    filename = upload_file.filename or "unnamed_file"
    dest = INCOMING_DIR / filename

    # מעתיקים את התוכן אל קובץ קבוע
    upload_file.file.seek(0)
    with open(dest, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    #  חשוב מאוד: להחזיר את הסמן להתחלה
    upload_file.file.seek(0)

    return str(dest)

