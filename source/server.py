from settings.base import URLS_DIR

from .url import UrlManager
from .wsgi import WSGIHandler

wsgi = WSGIHandler()

## configuration and check errors ##
# 1 - URL Manager:
UrlManager(wsgi=wsgi, directory_path=URLS_DIR).submit_urls()
