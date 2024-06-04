from server.app import Server
from server.url_manager import UrlManager
from settings.base import URLS_DIR

app = Server()

# URL Manager
try:
    UrlManager(server=app, directory_path=URLS_DIR).submit_urls()
    print(app.urls)

except Exception as e:
    print("--- An error occurred while routing URLs for the application.")
    print("--- For details, refer to the following error message:")
    print(f"-> ERROR MESSAGE: {str(e)}")
