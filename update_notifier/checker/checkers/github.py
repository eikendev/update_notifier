import json
import re

from abc import ABCMeta

from ..update_checker import UpdateChecker, UpdateCheckerException


class GithubUpdateChecker(UpdateChecker, metaclass=ABCMeta):
    URL_STATUS = ('https://api.github.com/repos/{owner}/{repo}/'
                  'releases/latest')
    URL_RELEASES = 'https://github.com/{}/{}/releases'
    version_pattern = re.compile(r'\d+\.\d+\.\d+')

    def get_status(self):
        url = self.URL_STATUS.format(owner=self.owner, repo=self.repo)
        page = self.load_url(url)

        try:
            obj = json.loads(page)
            tag = obj['tag_name']
        except json.JSONDecodeError:
            raise UpdateCheckerException('Retrieved invalid json.')

        version = re.search(self.version_pattern, tag)

        if version:
            version = version.group(0)
        else:
            raise UpdateCheckerException('Version not found.')

        # TODO: Find more elegant solution for asset.
        assets = obj['assets']
        asset = None

        for a in assets:
            if a['name'] == self.FILENAME:
                asset = a

        if asset is None:
            href = self.URL_RELEASES.format(self.owner, self.repo)
        else:
            href = asset['browser_download_url']

        return (version, href)
