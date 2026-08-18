# file type validators, safe-load helpers
import magic
from hashlib import sha256

ALLOWED_EXT = {
    ".pkl": "application/octet-stream",
    ".joblib": "application/octet-stream",
    ".h5": "application/x-hdf",
    ".pt": "application/octet-stream",
    ".onnx": "application/octet-stream"
}

def get_extension(filename: str):
    return "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

def allowed_file(filename: str) -> bool:
    ext = get_extension(filename)
    return ext in ALLOWED_EXT

def compute_sha256_bytes(data: bytes) -> str:
    h = sha256()
    h.update(data)
    return h.hexdigest()

# note: python-magic lib returns mime types
def mime_matches(data: bytes, filename: str) -> bool:
    try:
        m = magic.from_buffer(data, mime=True)
    except Exception:
        return False
    ext = get_extension(filename)
    expected = ALLOWED_EXT.get(ext)
    return expected is None or expected == m
