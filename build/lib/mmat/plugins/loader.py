# MMAT Plugin Loader
# Handles loading plugins from specified directories.

import importlib.util
import os

class PluginLoader:
    """
    Loads plugins from specified directories.
    """
    def __init__(self, plugin_dirs):
        self.plugin_dirs = plugin_dirs
        self.plugins = {}

    def load_plugins(self):
        """
        Loads all plugins from the configured directories.
        """
        for plugin_dir in self.plugin_dirs:
            if not os.path.isdir(plugin_dir):
                print(f"Warning: Plugin directory not found: {plugin_dir}")
                continue

            for item_name in os.listdir(plugin_dir):
                item_path = os.path.join(plugin_dir, item_name)
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                    # It's a package, try to load it as a plugin
                    try:
                        module_name = f"mmat.plugins.{item_name}" # Assuming plugins are within mmat.plugins
                        spec = importlib.util.spec_from_file_location(module_name, os.path.join(item_path, "__init__.py"))
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.plugins[item_name] = module
                        print(f"Loaded plugin: {item_name}")
                    except Exception as e:
                        print(f"Error loading plugin {item_name}: {e}")
                elif item_name.endswith(".py") and item_name != "__init__.py":
                    # It's a single file module, try to load it
                     try:
                        module_name = f"mmat.plugins.{item_name[:-3]}" # Assuming plugins are within mmat.plugins
                        spec = importlib.util.spec_from_file_location(module_name, item_path)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.plugins[item_name[:-3]] = module
                        print(f"Loaded plugin: {item_name[:-3]}")
                     except Exception as e:
                        print(f"Error loading plugin {item_name[:-3]}: {e}")


    def get_plugin(self, name):
        """
        Retrieves a loaded plugin by name.
        """
        return self.plugins.get(name)
