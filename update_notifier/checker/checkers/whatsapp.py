import re

from ..update_checker import UpdateChecker


class WhatsAppUpdateChecker(UpdateChecker):
    name = 'WhatsApp'
    fetch_url = 'https://www.whatsapp.com/android/'
    href_pattern = re.compile(r'http.*/WhatsApp\.apk')
    version_pattern = re.compile(r'Version (\d+\.\d+\.\d+)')

    def get_status(self):
        href = self.soup.find(href=self.href_pattern).get('href')
        version = self.soup(text=self.version_pattern)[0]
        version = self.version_pattern.match(version).group(1)

        return (version, href)
