from bitbucket import BitbucketDriver
from concourse import ConcourseResource

class BitbucketServerDriver(BitbucketDriver, ConcourseResource):
    def __init__(self, config: dict, debug: bool) -> None:
        self.debug = False
        self.username = ''
        self.password = ''
        self.endpoint = ''
        self.verify_ssl = False
        return
