from .github import GithubUpdateChecker


class MattermostUpdateChecker(GithubUpdateChecker):
    name = 'Mattermost'
    FILENAME = 'Mattermost.apk'
    owner = 'mattermost'
    repo = 'mattermost-mobile'
