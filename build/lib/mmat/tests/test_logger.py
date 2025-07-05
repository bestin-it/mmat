# MMAT Logger Tests
# Tests for the logging utility.

import unittest
import sys
from io import StringIO
from mmat.utils.logger import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        """Set up a StringIO object to capture stdout."""
        self._original_stdout = sys.stdout
        sys.stdout = self._stdout_capture = StringIO()

    def tearDown(self):
        """Restore original stdout."""
        sys.stdout = self._original_stdout

    def test_info_logging(self):
        """Test logging an info message."""
        logger = Logger()
        logger.info("This is an info message.")
        output = self._stdout_capture.getvalue().strip()
        self.assertIn("[INFO]", output)
        self.assertIn("This is an info message.", output)

    def test_warning_logging(self):
        """Test logging a warning message."""
        logger = Logger()
        logger.warning("This is a warning message.")
        output = self._stdout_capture.getvalue().strip()
        self.assertIn("[WARNING]", output)
        self.assertIn("This is a warning message.", output)

    def test_error_logging(self):
        """Test logging an error message."""
        logger = Logger()
        logger.error("This is an error message.")
        output = self._stdout_capture.getvalue().strip()
        self.assertIn("[ERROR]", output)
        self.assertIn("This is an error message.", output)

    def test_debug_logging_enabled(self):
        """Test logging a debug message when debug is enabled."""
        logger = Logger(debug=True)
        logger.debug("This is a debug message.")
        output = self._stdout_capture.getvalue().strip()
        self.assertIn("[DEBUG]", output)
        self.assertIn("This is a debug message.", output)

    def test_debug_logging_disabled(self):
        """Test logging a debug message when debug is disabled."""
        logger = Logger(debug=False)
        logger.debug("This is a debug message.")
        output = self._stdout_capture.getvalue().strip()
        self.assertEqual(output, "") # No output expected

    def test_multiple_messages(self):
        """Test logging multiple messages."""
        logger = Logger(debug=True)
        logger.info("Info 1")
        logger.debug("Debug 1")
        logger.warning("Warning 1")
        logger.error("Error 1")
        logger.info("Info 2")

        output_lines = self._stdout_capture.getvalue().strip().split('\n')

        self.assertEqual(len(output_lines), 5)
        self.assertIn("[INFO]", output_lines[0])
        self.assertIn("Info 1", output_lines[0])
        self.assertIn("[DEBUG]", output_lines[1])
        self.assertIn("Debug 1", output_lines[1])
        self.assertIn("[WARNING]", output_lines[2])
        self.assertIn("Warning 1", output_lines[2])
        self.assertIn("[ERROR]", output_lines[3])
        self.assertIn("Error 1", output_lines[3])
        self.assertIn("[INFO]", output_lines[4])
        self.assertIn("Info 2", output_lines[4])


if __name__ == '__main__':
    unittest.main()
