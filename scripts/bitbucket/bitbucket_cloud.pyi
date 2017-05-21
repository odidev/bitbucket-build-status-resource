from bitbucket import BitbucketDriver
from concourse import ConcourseResource

class BitbucketCloudDriver(BitbucketDriver, ConcourseResource):
    def __init__(self, config: dict, debug: bool) -> None:
        self.debug = False
        self.repository = ''
        self.client_id = ''
        self.client_secret = ''
        self.username = ''
        self.password = ''
        return
