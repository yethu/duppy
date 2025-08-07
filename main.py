from collections import defaultdict
import argparse
import hashlib
import os


def hash_file(path, chunk_size=8192):
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hasher.update(chunk)

    return hasher.hexdigest()


def find_duplicate_files(directory, recursive=True, chunk_size=8192):
    hash_to_files = defaultdict(list)

    if recursive:
        walker = os.walk(directory)
    else:
        walker = [(directory, [], os.listdir(directory))]

    for root, _, files in walker:
        for name in files:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                try:
                    file_hash = hash_file(path, chunk_size=chunk_size)
                    hash_to_files[file_hash].append(path)
                except (PermissionError, FileNotFoundError):
                    pass

    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}
    return duplicates


def validate_positive(value):
    v = int(value)
    if v <= 0:
        raise argparse.ArgumentTypeError(f"{v} is an invalid chunk size value")

    return v


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files using SHA-256 hashing."
    )
    parser.add_argument("directory", help="Path to the directory to scan")
    parser.add_argument(
        "--no-recursion",
        action="store_true",
        help="Limit the scan to top-level directories",
    )
    parser.add_argument(
        "--chunk-size",
        type=validate_positive,
        default=8192,
        help="Size (in bytes) of chunks to read when hashing files (default: 8192)",
    )
    args = parser.parse_args()

    duplicates = find_duplicate_files(args.directory, recursive=not args.no_recursion)

    if not duplicates:
        print("No duplicate files found.")
    else:
        print("Duplicate files found:")
        for file_hash, paths in duplicates.items():
            print(f"\nHash: {file_hash}")
            for path in paths:
                print(f"  - {path}")


if __name__ == "__main__":
    main()
