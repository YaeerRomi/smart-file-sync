import sys
from pathlib import Path
import hashlib as h


"""
Minimal demo: print the hash (hex) of a file.
Usage:
  python file_hash_demo.py /path/to/file
Example:
  python file_hash_demo.py ../test_files/my_resume.pdf
"""
CHUNK_BYTES = 8192

def hash_file(path: Path) -> str:
    algorithm = "Sha256"

    hash_alg = h.new(algorithm)

    with open(path, 'rb') as f: 
        while chunk := f.read(CHUNK_BYTES):
            hash_alg.update(chunk)

    return hash_alg.hexdigest()

    

def main(argv):
    if len(argv) < 2:
        print("Usage: python file_hash_demo.py <file> [algorithm]")
        return 1
     
    p = Path(argv[1])
    if not p.exists():
        print(f"Error: file not found: {p}", file=sys.stderr)
        return 1
    
    digest = hash_file(sys.argv[1])

    print(digest)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv))
