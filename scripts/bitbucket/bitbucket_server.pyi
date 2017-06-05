from bitbucket import BitbucketDriver
from concourse import ConcourseResource
from helper import CommitHash


class BitbucketServerDriver(BitbucketDriver, ConcourseResource):
    def __init__(self, config: dict, debug: bool) -> None:
        self.debug = False
        self.username = ''
        self.password = ''
        self.endpoint = ''
        self.verify_ssl = False
        return

    def get_post_url(self, commit_hash: CommitHash) -> str:
        return ''

    def get_request_options(self) -> dict:
        return {}

    def get_valid_response_status(self) -> list:
        return []
