import hashlib

def get_image_hash(data: bytes) -> str:
    """Return MD5 hash of image or SVG content."""
    return hashlib.md5(data).hexdigest()

def is_duplicate(hash_str: str, seen_hashes: set) -> bool:
    """Check and update seen hashes to detect duplicates."""
    return hash_str in seen_hashes
