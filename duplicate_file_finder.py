"""Find duplicate files by comparing SHA-256 hashes.

Safe by default: files are only deleted when --delete is provided.
Usage:
    python duplicate_file_finder.py "folder/path"
    python duplicate_file_finder.py "folder/path" --delete
"""
import argparse
import hashlib
import os
from collections import defaultdict
from pathlib import Path


def calculate_hash(file_path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 hash of a file's contents."""
    digest = hashlib.sha256()
    with file_path.open("rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(directory: Path) -> list[list[Path]]:
    """Return groups of files that have identical content."""
    hashes: dict[str, list[Path]] = defaultdict(list)

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            path = Path(root) / filename
            try:
                file_hash = calculate_hash(path)
                hashes[file_hash].append(path)
            except (OSError, PermissionError) as error:
                print(f"Skipped {path}: {error}")

    return [paths for paths in hashes.values() if len(paths) > 1]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find files with identical contents in a directory."
    )
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete duplicate copies after showing the groups. Keeps the first file in each group.",
    )
    args = parser.parse_args()

    directory = Path(args.directory).expanduser().resolve()
    if not directory.exists() or not directory.is_dir():
        parser.error(f"Not a valid directory: {directory}")

    groups = find_duplicates(directory)
    if not groups:
        print("No duplicate files found.")
        return

    print(f"Found {len(groups)} duplicate group(s):")
    for number, group in enumerate(groups, start=1):
        print(f"\nGroup {number}:")
        for index, path in enumerate(group):
            marker = "KEEP" if index == 0 else "DUPLICATE"
            print(f"  [{marker}] {path}")

    if not args.delete:
        print("\nPreview only. No files were deleted.")
        print("Review the results, then run again with --delete if appropriate.")
        return

    deleted = 0
    for group in groups:
        # Keep the first file found; remove the remaining identical copies.
        for duplicate in group[1:]:
            try:
                duplicate.unlink()
                print(f"Deleted: {duplicate}")
                deleted += 1
            except OSError as error:
                print(f"Could not delete {duplicate}: {error}")

    print(f"\nFinished. Deleted {deleted} duplicate file(s).")


if __name__ == "__main__":
    main()
