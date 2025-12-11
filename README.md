הנה **README.md מלא, נקי ו־מקצועי באנגלית בלבד**, מוכן להדבקה ל־GitHub או להגשה אקדמית.

---

# ✅ **README.md (English Version)**

```markdown
# 🛡️ MedSecure Gateway
MedSecure Gateway is a secure file-processing service designed to validate, scan, and upload documents in a controlled and auditable pipeline.  
It ensures that every uploaded file is safe, authentic, and properly stored.

---

## 🚀 Project Purpose

MedSecure Gateway acts as a security checkpoint for incoming files.  
Every file must successfully pass a strict validation pipeline:

1. **True MIME validation** (based on file content, not file extension)
2. **Antivirus scanning** using ClamAV (daemon mode)
3. **Checksum calculation** for integrity tracking
4. **Secure upload to AWS S3**
5. **Security Alert email** automatically sent when a step fails

Only if *all* steps succeed → the API returns `200 OK`.

---

## 🧩 Architecture Overview

```

Client → FastAPI Gateway → MIME Validation → ClamAV Antivirus Scan
↓
S3 Secure Upload
↓
Security Alert (on failure)

```

---

## 📁 Project Structure

```

MedSecure-Gateway/
│
├── server.py                     # Main FastAPI application
│
├── services/
│   ├── pipeline.py               # Orchestration of the validation pipeline
│   ├── mime_validation.py        # True MIME validation using python-magic
│   ├── antivirus.py              # ClamAV integration (UnixSocket + NetworkSocket fallback)
│   ├── s3_upload.py              # Upload handler for AWS S3
│   ├── alerting.py               # Security alert email generator
│
├── incoming/                     # Temporary storage for uploaded files
│
├── venv/                         # Python virtual environment
│
└── README.md

````

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-repo>/MedSecure-Gateway.git
cd MedSecure-Gateway
````

---

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 🛡️ ClamAV Setup (Ubuntu Server)

Install ClamAV and its daemon:

```bash
sudo apt update
sudo apt install clamav clamav-daemon -y
```

Update virus signatures:

```bash
sudo systemctl stop clamav-freshclam
sudo freshclam
sudo systemctl start clamav-daemon
sudo systemctl start clamav-freshclam
```

Check that ClamAV daemon is running:

```bash
sudo systemctl status clamav-daemon
```

---

## ☁️ AWS S3 Setup

Ensure AWS CLI is configured:

```bash
aws configure
```

Create your bucket:

```bash
aws s3api create-bucket \
  --bucket medsecure-eden-tma-2025 \
  --region eu-central-1 \
  --create-bucket-configuration LocationConstraint=eu-central-1
```

Update bucket name inside:

```
services/s3_upload.py
```

---

## ▶️ Run the FastAPI Server

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Open Swagger UI in the browser:

```
http://<server-ip>:8000/docs
```

---

## 📤 Example Successful Response

```json
{
  "received": true,
  "filename": "document.pdf",
  "checksum": "33D8C6BF..."
}
```

---

## ❗ Security Alerts

If any step fails (MIME, antivirus, S3 upload, etc.)
the system automatically generates a **Security Alert email**, containing:

* file name
* reason for failure
* timestamp
* diagnostic information

---

## 🔍 Troubleshooting

### ❌ `Unable to connect to ClamAV daemon`

Start the service manually:

```bash
sudo systemctl start clamav-daemon
```

---

### ❌ `NoSuchBucket`

Ensure the bucket name in your code matches the real AWS bucket.

---

### ❌ `python-magic: failed to find libmagic`

Install the system dependency:

```bash
sudo apt install libmagic1
```

---

## ✅ Status

✔️ Fully implemented validation pipeline
✔️ Antivirus scanning operational
✔️ S3 upload verified
✔️ Alerts functional
✔️ Production-style architecture

---

## 📄 License

This project is for academic use and security training purposes.

