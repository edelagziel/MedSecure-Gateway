import pathlib
from enum import Enum
from typing import Optional, Union

import pyclamd


class ScanStatus(str, Enum):
    CLEAN = "clean"
    INFECTED = "infected"
    ERROR = "error"   # Error during scan (daemon unavailable, file missing, etc.)


class AVScanResult:
    """
    Object representing the result of an antivirus scan:
    - status: CLEAN / INFECTED / ERROR
    - signature: the malware signature if detected, or an error description
    """

    def __init__(self, status: ScanStatus, signature: Optional[str] = None):
        self.status = status
        self.signature = signature

    def __repr__(self) -> str:
        return f"AVScanResult(status={self.status!r}, signature={self.signature!r})"


def _get_clamd_client() -> Union[pyclamd.ClamdUnixSocket, pyclamd.ClamdNetworkSocket]:
    """
    Connects to the ClamAV daemon.
    First attempts a Unix socket, then falls back to TCP (127.0.0.1:3310).
    Raises an exception if no connection is possible.
    """
    # Attempt 1: Unix socket (typical on Linux)
    try:
        cd = pyclamd.ClamdUnixSocket()
        cd.ping()
        return cd
    except Exception:
        pass

    # Attempt 2: TCP socket
    cd = pyclamd.ClamdNetworkSocket(host="127.0.0.1", port=3310)
    cd.ping()  # Will raise an exception if the daemon is unreachable
    return cd


def scan_file(file_path: str) -> AVScanResult:
    """
    Scan a file using a ClamAV daemon via pyClamd.

    Returns:
      - AVScanResult(ScanStatus.CLEAN)
            → File is clean, safe to proceed (e.g., upload to S3)
      - AVScanResult(ScanStatus.INFECTED, "Signature-Name")
            → Malware detected; DO NOT upload to S3
      - AVScanResult(ScanStatus.ERROR, "reason")
            → Scan failed; treat as unsafe (fail-safe: DO NOT upload)
    """
    path = pathlib.Path(file_path)

    if not path.is_file():
        return AVScanResult(
            status=ScanStatus.ERROR,
            signature="file_not_found",
        )

    # Connect to ClamAV daemon
    try:
        cd = _get_clamd_client()
    except Exception as e:
        return AVScanResult(
            status=ScanStatus.ERROR,
            signature=f"clamd_connection_error: {e}",
        )

    # ClamAV returns a dict like:
    # {'/full/path/to/file': ('FOUND', 'Eicar-Test-Signature')}
    try:
        result = cd.scan_file(str(path))
    except Exception as e:
        return AVScanResult(
            status=ScanStatus.ERROR,
            signature=f"scan_error: {e}",
        )

    # result == None → no malware detected
    if result is None:
        return AVScanResult(status=ScanStatus.CLEAN)

    # Extract verdict and signature from the dictionary
    verdict, signature = list(result.values())[0]  # verdict: 'FOUND' / 'OK' / etc.
    verdict = verdict.lower()

    if verdict == "found":
        # Malware detected → DO NOT upload to S3
        return AVScanResult(
            status=ScanStatus.INFECTED,
            signature=signature,
        )

    # Any unexpected verdict is treated as an error/suspicious (fail-safe)
    return AVScanResult(
        status=ScanStatus.ERROR,
        signature=f"unexpected_verdict:{verdict}:{signature}",
    )
