import unittest
import tempfile
import os
import hashlib
from main import hash_file


class TestHashFile(unittest.TestCase):
    def test_hash_file_known_content(self):
        content = b'hello world'
        expected_hash = hashlib.sha256(content).hexdigest()

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            self.assertEqual(hash_file(tmp_path), expected_hash)
        finally:
            os.remove(tmp_path)


if __name__ == '__main__':
    unittest.main()
