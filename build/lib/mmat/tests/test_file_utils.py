# MMAT File Utils Tests
# Tests for the file utility functions.

import unittest
import os
import shutil
from mmat.utils.file_utils import find_files_by_pattern, read_file_content

# Define a temporary directory for testing file utilities
TEST_DIR = "test_file_utils_dir"

class TestFileUtils(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and files for testing."""
        os.makedirs(TEST_DIR, exist_ok=True)
        os.makedirs(os.path.join(TEST_DIR, "subdir"), exist_ok=True)

        # Create test files
        with open(os.path.join(TEST_DIR, "file1.txt"), 'w') as f:
            f.write("Content of file1.txt")
        with open(os.path.join(TEST_DIR, "file2.log"), 'w') as f:
            f.write("Content of file2.log")
        with open(os.path.join(TEST_DIR, "another_file.txt"), 'w') as f:
            f.write("Another text file")
        with open(os.path.join(TEST_DIR, "subdir", "subfile.txt"), 'w') as f:
            f.write("Content of subfile.txt")
        with open(os.path.join(TEST_DIR, "subdir", "subfile.data"), 'w') as f:
            f.write("Binary data")

    def tearDown(self):
        """Clean up the temporary directory."""
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def test_find_files_by_pattern_txt(self):
        """Test finding files with a specific pattern (*.txt)."""
        found_files = find_files_by_pattern(TEST_DIR, "*.txt")
        # Sort for consistent comparison
        found_files.sort()

        expected_files = [
            os.path.join(TEST_DIR, "another_file.txt"),
            os.path.join(TEST_DIR, "file1.txt"),
            os.path.join(TEST_DIR, "subdir", "subfile.txt")
        ]
        expected_files.sort()

        self.assertEqual(found_files, expected_files)

    def test_find_files_by_pattern_all(self):
        """Test finding all files in the directory."""
        found_files = find_files_by_pattern(TEST_DIR, "*")
        found_files.sort()

        expected_files = [
            os.path.join(TEST_DIR, "another_file.txt"),
            os.path.join(TEST_DIR, "file1.txt"),
            os.path.join(TEST_DIR, "file2.log"),
            os.path.join(TEST_DIR, "subdir", "subfile.data"),
            os.path.join(TEST_DIR, "subdir", "subfile.txt")
        ]
        expected_files.sort()

        self.assertEqual(found_files, expected_files)

    def test_find_files_by_pattern_non_existent(self):
        """Test finding files with a pattern that doesn't match anything."""
        found_files = find_files_by_pattern(TEST_DIR, "*.json")
        self.assertEqual(found_files, [])

    def test_find_files_directory_not_found(self):
        """Test finding files in a non-existent directory."""
        found_files = find_files_by_pattern("non_existent_dir", "*.txt")
        self.assertEqual(found_files, [])

    def test_read_file_content_success(self):
        """Test reading content from an existing file."""
        file_path = os.path.join(TEST_DIR, "file1.txt")
        content = read_file_content(file_path)
        self.assertEqual(content, "Content of file1.txt")

    def test_read_file_content_non_existent(self):
        """Test reading content from a non-existent file."""
        file_path = os.path.join(TEST_DIR, "non_existent_file.txt")
        content = read_file_content(file_path)
        self.assertIsNone(content) # Or handle as an exception depending on implementation

    def test_read_file_content_empty_file(self):
        """Test reading content from an empty file."""
        empty_file_path = os.path.join(TEST_DIR, "empty_file.txt")
        with open(empty_file_path, 'w') as f:
            pass # Create an empty file

        content = read_file_content(empty_file_path)
        self.assertEqual(content, "")


if __name__ == '__main__':
    unittest.main()
