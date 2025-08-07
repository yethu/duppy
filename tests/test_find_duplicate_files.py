import tempfile
import shutil
import os
from main import find_duplicate_files


def test_find_duplicate_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create duplicate files
        file1 = os.path.join(tmpdir, "a.txt")
        file2 = os.path.join(tmpdir, "b.txt")
        file3 = os.path.join(tmpdir, "c.txt")  # different content

        with open(file1, "w") as f:
            f.write("duplicate content")

        with open(file2, "w") as f:
            f.write("duplicate content")

        with open(file3, "w") as f:
            f.write("unique content")

        duplicates = find_duplicate_files(tmpdir)

        # All duplicates should share the same hash and include file1 and file2
        all_duplicate_files = [set(paths) for paths in duplicates.values()]
        expected = {file1, file2}

        assert any(expected.issubset(group) for group in all_duplicate_files)
