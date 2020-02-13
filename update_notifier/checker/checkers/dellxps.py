import json
import re

from urllib.parse import urlparse

from ..update_checker import UpdateChecker, UpdateCheckerException


class DellXPSUpdateChecker(UpdateChecker):
    name = 'Dell XPS'
    URL_STATUS = ('https://www.dell.com/support/home/at/de/atbsdt1/drivers/'
                  'driverslist/platfromdriver?productCode=xps-13-9360-laptop'
                  '&osCode=BIOSA&isTagResult=false')
    version_pattern = re.compile(r'\d+\.\d+\.\d+')

    def get_status(self):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        page = self.load_url(self.URL_STATUS, headers=headers)

        try:
            obj = json.loads(page)
            driver_list_s = obj['DriverListData']
            driver_list = json.loads(driver_list_s)
        except json.JSONDecodeError:
            raise UpdateCheckerException('Retrieved invalid json.')

        for d in driver_list:
            if d['cat'] == 'BI':
                driver = d

        if driver is None:
            raise UpdateCheckerException('Driver not found.')

        href = driver['fileFrmtInfo']['httpFileLocation']
        path = urlparse(href).path
        filename = path.split('/')[-1]
        version = re.search(self.version_pattern, filename)

        if version:
            version = version.group(0)
        else:
            raise UpdateCheckerException('Version not found.')

        return (version, href)
