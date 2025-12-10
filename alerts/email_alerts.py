from datetime import datetime, timezone
from email.mime.text import MIMEText


ALERT_EMAIL = "security.manager@example.com"   # For the assignment
SENDER_EMAIL = "gateway-alerts@example.com"    # Fake sender address


def send_security_alert(filename: str, reason: str):
    """
    Generates a security alert for suspicious or failed file validation events.
    """

    timestamp = datetime.now(timezone.utc).isoformat()

    # Build message content
    message_body = (
        f"Security Alert Triggered!\n\n"
        f"File: {filename}\n"
        f"Timestamp: {timestamp} UTC\n"
        f"Reason: {reason}\n"
    )

    msg = MIMEText(message_body)
    msg["Subject"] = f"[ALERT] Suspicious File Detected: {filename}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = ALERT_EMAIL

    # For the assignment: no SMTP needed.
    print("\n--- SECURITY ALERT ---")
    print(msg.as_string())
    print("----------------------\n")

    return {
        "filename": filename,
        "timestamp": timestamp,
        "reason": reason
    }
