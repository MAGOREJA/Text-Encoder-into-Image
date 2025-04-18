import hashlib

def load_signatures(signature_file="signatures.txt"):
    """Load malware signatures from a file."""
    with open(signature_file, "r") as file:
        return [line.strip() for line in file]

def calculate_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")

def scan_file(file_path, signatures):
    """Scan a file for malware."""
    file_hash = calculate_file_hash(file_path)
    if file_hash in signatures:
        return True, file_hash  # Infected
    return False, None  # Clean