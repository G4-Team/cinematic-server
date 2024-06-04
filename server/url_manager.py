import importlib.util
import os


class UrlManager:
    def __init__(self, server, directory_path) -> None:
        self.server = server
        self.directory_path = directory_path

    def import_module_from_file(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def submit_urls(self):
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(self.directory_path, filename)

                module_name = filename[:-3]
                module = self.import_module_from_file(module_name, file_path)

                var_name = f"{module_name}_urls"

                if hasattr(module, var_name):
                    variable_value = getattr(module, var_name)
                    self.server.urls.update(variable_value)
