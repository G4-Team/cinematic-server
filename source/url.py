import importlib.util
import os

from settings.base import APPS, BASE_DIR


class UrlManager:
    def __init__(self, wsgi, directory_path) -> None:
        self.wsgi = wsgi
        self.directory_path = directory_path

    def import_module_from_file(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def submit_urls(self):
        for app in APPS:
            file_path = os.path.join(BASE_DIR / app, "urls.py")
            module_name = "urls"
            module = self.import_module_from_file(module_name, file_path)

            var_name = f"{app}_urls"

            if hasattr(module, var_name):
                variable_value = getattr(module, var_name)
                for key, value in variable_value.items():
                    self.wsgi.urls[f"/{app}/{key}"] = value
