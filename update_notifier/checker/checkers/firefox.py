import requests

from requests.exceptions import RequestException
from urllib.parse import urlparse

from ..update_checker import UpdateChecker, UpdateCheckerException


class FirefoxUpdateChecker(UpdateChecker):
    name = 'Firefox'
    fetch_url = ('https://download.mozilla.org/'
                 '?product=fennec-latest&os=android&lang=multi')

    def get_status(self):
        try:
            href = requests.head(self.fetch_url, allow_redirects=True).url
        except (RequestException, ConnectionError):
            raise UpdateCheckerException()

        path = urlparse(href).path
        parts = path.split('/')

        if len(parts) < 4:
            raise UpdateCheckerException()

        version = path.split('/')[-4]
        return (version, href)
