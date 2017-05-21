from bitbucket import BitbucketDriver
from requests.auth import AuthBase
from requests import request

def set_build_status(commit_hash: str, build_status: str, key: str, name: str, url: str, description: str, debug: bool, driver: BitbucketDriver) -> None:
    return

def request_access_token(client_id: str, secret: str, debug: bool) -> str:
    return ''

class BitbucketException(Exception):
    pass

class BitbucketOAuth(AuthBase):
    def __init__(self, access_token: str) -> None:
        self.access_token = ''
        return

    def __call__(self, request: request) -> request:
        return request

class BitbucketDriver(object):
    def __init__(self, config: dict) -> None:
        return

    def get_post_url(self, commit_hash: str) -> str:
        return ''

    def get_request_options(self) -> dict:
        return {}

    def get_valid_response_status(self) -> list:
        return []
