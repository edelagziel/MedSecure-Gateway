import pathlib
import pyclamd

def scan_file(file_path: str):
    """
    Scan a file with ClamAV. Raises an Exception if infected or on error.
    """
    path = pathlib.Path(file_path)

    if not path.is_file():
        raise ValueError("File not found for antivirus scan")

    # Try connecting to ClamAV daemon
    try:
        try:
            cd = pyclamd.ClamdUnixSocket()
            cd.ping()
        except Exception:
            cd = pyclamd.ClamdNetworkSocket(host="127.0.0.1", port=3310)
            cd.ping()
    except Exception:
        raise ValueError("Unable to connect to ClamAV daemon")

    # Actual scan
    try:
        result = cd.scan_file(str(path))
    except Exception as e:
        raise ValueError(f"Antivirus scan error: {e}")

    # If result is None → clean
    if result is None:
        return True

    # result looks like: {'/path': ('FOUND', 'Eicar-Test-Signature')}
    verdict, signature = list(result.values())[0]

    if verdict.lower() == "found":
        raise ValueError(f"Virus detected: {signature}")

    # Any unknown verdict treated as suspicious
    raise ValueError(f"Unexpected scan result: {verdict}")
