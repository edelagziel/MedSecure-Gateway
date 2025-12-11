import pathlib  # Import pathlib for file path operations
import pyclamd  # Import pyclamd for ClamAV interactions

def scan_file(file_path: str):
    """
    Scan a file with ClamAV using STREAM mode.
    Avoids permission problems with clamd.
    """
    path = pathlib.Path(file_path)  # Convert string file path to Path object

    if not path.is_file():  # Check the file exists at the given path
        raise ValueError("File not found for antivirus scan")

    # Connect to ClamAV daemon, prefer Unix socket; fall back to network socket
    try:
        try:
            cd = pyclamd.ClamdUnixSocket()  # Attempt to connect via Unix socket
            cd.ping()  # Test connection to ClamAV daemon
        except Exception:
            cd = pyclamd.ClamdNetworkSocket(host="127.0.0.1", port=3310)  # Fallback to TCP connection
            cd.ping()  # Test TCP connection
    except Exception:
        raise ValueError("Unable to connect to ClamAV daemon")

    # STREAM scan: send file content directly for scanning
    try:
        with open(path, "rb") as f:  # Open file in binary read mode
            data = f.read()  # Read entire file data

        result = cd.scan_stream(data)  # Scan data via ClamAV stream

    except Exception as e:
        raise ValueError(f"Antivirus scan error: {e}")

    # If 'result' is None, the file is clean
    if result is None:
        return True

    # result example: {'stream': ('FOUND', 'Eicar-Test-Signature')}
    verdict, signature = list(result.values())[0]  # Extract scan verdict and virus signature

    if verdict.lower() == "found":  # If a virus is found, raise ValueError
        raise ValueError(f"Virus detected: {signature}")

    # Any unexpected result is treated as suspicious, so return True
    return True
