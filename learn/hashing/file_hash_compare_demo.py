import sys
from pathlib import Path
import hashlib as h


"""
Minimal demo: compare two files by hash.
Usage:
  python file_hash_compare_demo.py fileA fileB 
Example:
  python file_hash_compare_demo.py a.txt b.txt
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
     
    f1 = Path(argv[1])
    f2 = Path(argv[2])

    for p in (f1, f2):
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 1


    h1 = hash_file(sys.argv[1])
    h2 = hash_file(sys.argv[2])
    if h1 == h2:
        print("IDENTICAL")
        print(f"{f1}: {h1}")
        print(f"{f2}: {h2}")
        return 0
    else:
        print("DIFFER")
        print(f"{f1}: {h1}")
        print(f"{f2}: {h2}")
        return 2


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv))
