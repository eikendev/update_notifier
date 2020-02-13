from .github import GithubUpdateChecker


class LichobileUpdateChecker(GithubUpdateChecker):
    name = 'lichobile'
    FILENAME = 'app-release.apk'
    owner = 'veloce'
    repo = 'lichobile'
