import functools
import logging

from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from socket import timeout
from urllib.error import URLError
from urllib.request import Request, urlopen


class UpdateChecker(metaclass=ABCMeta):
    def __init__(self):
        status = self.get_status()
        self.version = status[0]
        self.href = status[1]

    def is_new_update(self, versions):
        if not versions:
            raise ValueError('Versions must not be None.')
        elif type(versions) is not dict:
            raise TypeError('Versions must be of type dict.')

        if self.name not in versions:
            # first time running this update checker
            return True
        else:
            cached_version = versions[self.name]

        logging.debug("%s: new version: %s\t old version: %s",
                      self.name, self.version, cached_version)

        new_version = Version(self.version)
        old_version = Version(cached_version)

        return new_version > old_version

    @property
    def soup(self):
        page = self.load_url(self.fetch_url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    @staticmethod
    def load_url(url, headers=dict()):
        req = Request(url, headers=headers)

        try:
            with urlopen(req, timeout=10) as page:
                page = page.read().decode('UTF-8')

            return page
        except (URLError, ConnectionError, timeout):
            raise UpdateCheckerException()

    @abstractmethod
    def get_status(self):
        """
        Returns a tuple containing the current version and the download link.
        """


class UpdateCheckerException(Exception):
    pass


@functools.total_ordering
class Version:
    def __init__(self, version_raw):
        self.version = version_raw.split('.')

        try:
            self.version = [int(x) for x in self.version]
            self.degree = len(self.version)
        except ValueError:
            self.version = version_raw
            self.degree = 0

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        if self.degree != other.degree:
            return False

        if self.degree == 0:
            return self.version == other.version

        for k in range(self.degree):
            if self.version[k] != other.version[k]:
                return False

        return True

    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        # missing subversion is turned to `0` implicitly
        if self.degree > other.degree:
            diff = self.degree - other.degree
            other.version += [0 for x in range(diff)]
        elif self.degree < other.degree:
            diff = other.degree - self.degree
            other.version += [0 for x in range(diff)]

        if self.degree == 0:
            return self.version > other.version

        for k in range(self.degree - 1):
            if self.version[k] > other.version[k]:
                return True
            elif self.version[k] < other.version[k]:
                return False

        # previous indexes were equal
        if self.version[-1] <= other.version[-1]:
            return False

        return True
