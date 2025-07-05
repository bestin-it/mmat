import yaml
import os

class ConfigLoader:
    """
    Loads configuration from a YAML file.
    """
    def __init__(self):
        self.config = {}

    def load_config(self, config_path):
        """
        Loads the configuration from the specified YAML file.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration dictionary.

        Raises:
            FileNotFoundError: If the config file does not exist.
            yaml.YAMLError: If there is an error parsing the YAML file.
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            return self.config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing configuration file {config_path}: {e}")

    def get(self, key, default=None):
        """
        Gets a value from the configuration using a dot-separated key.

        Args:
            key (str): The dot-separated key (e.g., "logging.level").
            default: The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value if not found.
        """
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    # Create a dummy config file for testing
    dummy_config_content = """
logging:
  level: DEBUG
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

plugins:
  paths:
    - ./plugins
    - ./custom_plugins

reporting:
  reporters:
    - type: json_reporter
      config:
        output_file: results.json
    - type: html_reporter
      config:
        output_dir: html_reports

environment:
  type: browser_environment
  config:
    browser: chrome
    headless: false
"""
    with open("dummy_config.yaml", "w") as f:
        f.write(dummy_config_content)

    loader = ConfigLoader()
    try:
        config = loader.load_config("dummy_config.yaml")
        print("Config loaded successfully:")
        print(config)

        print("\nGetting values:")
        print(f"Logging level: {loader.get('logging.level')}")
        print(f"First plugin path: {loader.get('plugins.paths.0')}")
        print(f"HTML reporter output dir: {loader.get('reporting.reporters.1.config.output_dir')}")
        print(f"Non-existent key: {loader.get('non_existent.key', 'default_value')}")

    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error loading config: {e}")
    finally:
        # Clean up the dummy config file
        if os.path.exists("dummy_config.yaml"):
            os.remove("dummy_config.yaml")
