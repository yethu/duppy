from collections import defaultdict
import argparse
import hashlib
import os


def hash_file(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)

    return hasher.hexdigest()


def find_duplicate_files(directory):
    hash_to_files = defaultdict(list)

    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                file_hash = hash_file(path)
                hash_to_files[file_hash].append(path)
            except (PermissionError, FileNotFoundError):
                pass

    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}
    return duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files using SHA-256 hashing."
    )
    parser.add_argument("directory", help="Path to the directory to scan")
    args = parser.parse_args()

    duplicates = find_duplicate_files(args.directory)

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
