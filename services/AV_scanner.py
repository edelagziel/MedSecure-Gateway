import pathlib
import pyclamd

def scan_file(file_path: str):
    """
    Scan a file with ClamAV using STREAM mode.
    Avoids permission problems with clamd.
    """
    path = pathlib.Path(file_path)

    if not path.is_file():
        raise ValueError("File not found for antivirus scan")

    # Connect to ClamAV daemon
    try:
        try:
            cd = pyclamd.ClamdUnixSocket()
            cd.ping()
        except Exception:
            cd = pyclamd.ClamdNetworkSocket(host="127.0.0.1", port=3310)
            cd.ping()
    except Exception:
        raise ValueError("Unable to connect to ClamAV daemon")

    # STREAM scan (recommended)
    try:
        with open(path, "rb") as f:
            data = f.read()

        result = cd.scan_stream(data)

    except Exception as e:
        raise ValueError(f"Antivirus scan error: {e}")

    # If result is None → clean
    if result is None:
        return True

    # result example: {'stream': ('FOUND', 'Eicar-Test-Signature')}
    verdict, signature = list(result.values())[0]

    if verdict.lower() == "found":
        raise ValueError(f"Virus detected: {signature}")

    # Any unexpected result is treated as suspicious
    return True
