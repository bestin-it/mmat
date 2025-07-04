import os
import yaml
import json

class ConfigManager:
    """
    Handles loading and managing configuration for the MMAT framework.
    """
    def __init__(self, config_path=None):
        """
        Initializes the ConfigManager.

        Args:
            config_path (str, optional): Path to the configuration file (YAML or JSON).
                                         Defaults to None, in which case a default config is used.
        """
        self.config = {}
        self.config_path = config_path
        print("[ConfigManager] Initialized.")
        if config_path:
            self.load_config(config_path)
        else:
            self._load_default_config()

    def load_config(self, config_path):
        """
        Loads configuration from a specified file.

        Args:
            config_path (str): Path to the configuration file (YAML or JSON).
        """
        if not os.path.exists(config_path):
            print(f"[ConfigManager] Warning: Configuration file not found at {config_path}. Using default config.")
            self._load_default_config()
            return

        _, file_extension = os.path.splitext(config_path)
        file_extension = file_extension.lower()

        try:
            with open(config_path, 'r') as f:
                if file_extension in ['.yaml', '.yml']:
                    self.config = yaml.safe_load(f)
                elif file_extension == '.json':
                    self.config = json.load(f)
                else:
                    print(f"[ConfigManager] Warning: Unsupported file format for config: {file_extension}. Using default config.")
                    self._load_default_config()
                    return

            print(f"[ConfigManager] Successfully loaded configuration from {config_path}")
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            print(f"[ConfigManager] Error parsing configuration file {config_path}: {e}. Using default config.")
            self._load_default_config()
        except Exception as e:
            print(f"[ConfigManager] An unexpected error occurred while loading {config_path}: {e}. Using default config.")
            self._load_default_config()

    def _load_default_config(self):
        """
        Loads a default configuration.
        """
        print("[ConfigManager] Loading default configuration.")
        self.config = {
            "driver": {
                "type": "playwright",
                "browser": "chromium",
                "headless": True
            },
            "test_plans_dir": "test_plans",
            "output_dir": "output"
            # Add other default configuration settings as needed
        }

    def get(self, key, default=None):
        """
        Gets a configuration value by key. Supports nested keys using dot notation (e.g., 'driver.browser').

        Args:
            key (str): The configuration key.
            default: The default value to return if the key is not found.

        Returns:
            The configuration value, or the default value if not found.
        """
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        """
        Sets a configuration value by key. Supports nested keys using dot notation (e.g., 'driver.browser').

        Args:
            key (str): The configuration key.
            value: The value to set.
        """
        keys = key.split('.')
        d = self.config
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value
        print(f"[ConfigManager] Set config key '{key}' to '{value}'")

    # Add other methods for saving config, validating config, etc.
