# MMAT Plugin Loader Tests
# Tests for the plugin loading utility.

import unittest
import os
import sys
import shutil
from mmat.plugins.loader import PluginLoader
from mmat.plugins.base_plugin import BasePlugin

# Define a temporary directory for mock plugins
MOCK_PLUGINS_DIR = "mock_plugins"

# Create a mock plugin file content
MOCK_PLUGIN_CONTENT_VALID = """
from mmat.plugins.base_plugin import BasePlugin

class MockPlugin(BasePlugin):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "MockPlugin"
        self.description = "A mock plugin for testing."

    def run(self):
        return "MockPlugin executed"

    def configure(self, config):
        self.config = config
        return True
"""

# Create a mock plugin file content with an invalid class name
MOCK_PLUGIN_CONTENT_INVALID_NAME = """
from mmat.plugins.base_plugin import BasePlugin

class WrongName(BasePlugin): # Class name doesn't match file name
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "WrongNamePlugin"
        self.description = "A mock plugin with wrong name."

    def run(self):
        return "WrongNamePlugin executed"

    def configure(self, config):
        self.config = config
        return True
"""

# Create a mock plugin file content with a syntax error
MOCK_PLUGIN_CONTENT_SYNTAX_ERROR = """
from mmat.plugins.base_plugin import BasePlugin

class SyntaxErrorPlugin(BasePlugin):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "SyntaxErrorPlugin"
        self.description = "A mock plugin with syntax error."

    def run(self):
        return "SyntaxErrorPlugin executed"

    def configure(self, config):
        self.config = config
        return True

    def invalid_method( # Missing closing parenthesis
"""

# Create a mock plugin file content that doesn't inherit from BasePlugin
MOCK_PLUGIN_CONTENT_NO_INHERITANCE = """
class NotAPlugin:
    def __init__(self, config=None):
        self.name = "NotAPlugin"
        self.description = "Not a plugin."

    def run(self):
        return "NotAPlugin executed"
"""


class TestPluginLoader(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and mock plugin files for testing."""
        os.makedirs(MOCK_PLUGINS_DIR, exist_ok=True)

        # Create valid mock plugin file
        with open(os.path.join(MOCK_PLUGINS_DIR, "mock_plugin.py"), 'w') as f:
            f.write(MOCK_PLUGIN_CONTENT_VALID)

        # Create invalid mock plugin file (wrong name)
        with open(os.path.join(MOCK_PLUGINS_DIR, "invalid_name_plugin.py"), 'w') as f:
            f.write(MOCK_PLUGIN_CONTENT_INVALID_NAME)

        # Create invalid mock plugin file (syntax error)
        with open(os.path.join(MOCK_PLUGINS_DIR, "syntax_error_plugin.py"), 'w') as f:
            f.write(MOCK_PLUGIN_CONTENT_SYNTAX_ERROR)

        # Create invalid mock plugin file (no inheritance)
        with open(os.path.join(MOCK_PLUGINS_DIR, "no_inheritance_plugin.py"), 'w') as f:
            f.write(MOCK_PLUGIN_CONTENT_NO_INHERITANCE)

        # Add the mock plugins directory to sys.path so imports work
        sys.path.insert(0, MOCK_PLUGINS_DIR)


    def tearDown(self):
        """Clean up the temporary directory and remove from sys.path."""
        if os.path.exists(MOCK_PLUGINS_DIR):
            shutil.rmtree(MOCK_PLUGINS_DIR)
        if MOCK_PLUGINS_DIR in sys.path:
            sys.path.remove(MOCK_PLUGINS_DIR)

    def test_load_plugins_success(self):
        """Test successful loading of valid plugins."""
        loader = PluginLoader(MOCK_PLUGINS_DIR)
        plugins = loader.load_plugins()

        self.assertIsInstance(plugins, list)
        self.assertEqual(len(plugins), 1) # Only one valid plugin expected

        plugin = plugins[0]
        self.assertIsInstance(plugin, BasePlugin)
        self.assertEqual(plugin.name, "MockPlugin")
        self.assertEqual(plugin.description, "A mock plugin for testing.")

    def test_load_plugins_directory_not_found(self):
        """Test loading plugins from a non-existent directory."""
        loader = PluginLoader("non_existent_plugins")
        plugins = loader.load_plugins()

        self.assertIsInstance(plugins, list)
        self.assertEqual(len(plugins), 0) # No plugins should be loaded

    def test_load_plugins_invalid_files(self):
        """Test handling of invalid plugin files (syntax errors, wrong class name, no inheritance)."""
        # The setUp creates invalid files. We just need to load and check the count.
        loader = PluginLoader(MOCK_PLUGINS_DIR)
        plugins = loader.load_plugins()

        self.assertIsInstance(plugins, list)
        self.assertEqual(len(plugins), 1) # Only the valid plugin should be loaded

        plugin = plugins[0]
        self.assertIsInstance(plugin, BasePlugin)
        self.assertEqual(plugin.name, "MockPlugin")


if __name__ == '__main__':
    unittest.main()
