# MMAT Config Loader Tests
# Tests for the configuration loading utility.

import unittest
import os
import json
from mmat.config.loader import ConfigLoader

class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        """Set up a temporary config file for testing."""
        self.test_config_dir = "test_config"
        self.test_config_file = os.path.join(self.test_config_dir, "config.json")
        os.makedirs(self.test_config_dir, exist_ok=True)
        self.config_data = {
            "setting1": "value1",
            "setting2": 123,
            "nested": {
                "setting3": True
            }
        }
        with open(self.test_config_file, 'w') as f:
            json.dump(self.config_data, f)

    def tearDown(self):
        """Clean up the temporary config file and directory."""
        os.remove(self.test_config_file)
        os.rmdir(self.test_config_dir)

    def test_load_config_success(self):
        """Test successful loading of a config file."""
        loader = ConfigLoader(self.test_config_file)
        config = loader.load_config()
        self.assertIsNotNone(config)
        self.assertEqual(config, self.config_data)

    def test_load_config_file_not_found(self):
        """Test loading a non-existent config file."""
        loader = ConfigLoader("non_existent_file.json")
        config = loader.load_config()
        self.assertIsNone(config)

    def test_load_config_invalid_json(self):
        """Test loading a config file with invalid JSON."""
        invalid_json_file = os.path.join(self.test_config_dir, "invalid.json")
        with open(invalid_json_file, 'w') as f:
            f.write("{invalid json}")
        loader = ConfigLoader(invalid_json_file)
        config = loader.load_config()
        self.assertIsNone(config)
        os.remove(invalid_json_file)

if __name__ == '__main__':
    unittest.main()
