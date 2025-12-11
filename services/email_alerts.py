from datetime import datetime, timezone    # Import datetime for timestamps, timezone for UTC
from email.mime.text import MIMEText       # Import MIMEText for composing email alerts

ALERT_EMAIL = "security.manager@example.com"   # Recipient of security alerts (assignment placeholder)
SENDER_EMAIL = "gateway-alerts@example.com"    # Sender address for alerts (fake for assignment)

def send_security_alert(filename: str, reason: str):
    """
    Generates a security alert for suspicious or failed file validation events.
    """
    timestamp = datetime.now(timezone.utc).isoformat()   # Get current UTC timestamp in ISO format

    # Construct the message body for the alert
    message_body = (
        f"Security Alert Triggered!\n\n"
        f"File: {filename}\n"
        f"Timestamp: {timestamp} UTC\n"
        f"Reason: {reason}\n"
    )

    msg = MIMEText(message_body)                         # Create a MIMEText email message with the body
    msg["Subject"] = f"[ALERT] Suspicious File Detected: {filename}"  # Set email subject
    msg["From"] = SENDER_EMAIL                           # Set sender email
    msg["To"] = ALERT_EMAIL                              # Set recipient email

    # For the assignment: Simulate sending the alert (print instead of emailing)
    print("\n--- SECURITY ALERT ---")
    print(msg.as_string())                               # Print the constructed alert email message
    print("----------------------\n")

    # return {
    #     "filename": filename,
    #     "timestamp": timestamp,
    #     "reason": reason
    # }

    # not using the value of return so not needed 
