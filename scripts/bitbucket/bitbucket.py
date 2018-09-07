import requests
from abc import ABCMeta, abstractmethod
from concourse import print_error
from helper import json_pp
from requests.auth import HTTPBasicAuth, AuthBase

ERROR_MAP = {
    403: "HTTP 403 Forbidden - Does your Bitbucket user have rights to the repository?",
    404: "HTTP 404 Not Found - Does the repository supplied exist?",
    401: "HTTP 401 Unauthorized - Are your Bitbucket credentials correct?",
    400: "HTTP 400 Bad Request - something's gone wrong. Set `source.debug: true` to show details"
}


class BitbucketException(Exception):
    pass


class BitbucketDriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config):
        return

    @abstractmethod
    def get_post_url(self, commit_hash):
        return ''

    @abstractmethod
    def get_request_options(self):
        return {}

    @abstractmethod
    def get_valid_response_status(self):
        return []


class BitbucketOAuth(AuthBase):
    """
        Adds the correct auth token for OAuth access to bitbucket.com
    """
    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, request):
        request.headers['Authorization'] = "Bearer {}".format(self.access_token)
        return request


def set_build_status(commit_hash, build_status, key, name, url, description, debug, driver):

    post_url = driver.get_post_url(commit_hash)

    data = {
        "state": build_status,
        "key": key,
        "name": name,
        "url": url,
        "description": description
    }

    if debug:
        print_error("Set build status: " + str(data))

    response = requests.post(
        post_url,
        json=data,
        **driver.get_request_options()
    )

    if debug:
        print_error("Request result: " + str(response.json()))

    # Check status code. Bitbucket brakes rest a bit  by returning 200 or 201
    # depending on it's the first time the status is posted.
    if response.status_code not in driver.get_valid_response_status():
        try:
            message = ERROR_MAP[response.status_code]
        except KeyError:
            message = json_pp(response.json())

        raise BitbucketException(message)


def request_access_token(client_id, secret, debug):
    response = requests.post(
        'https://bitbucket.org/site/oauth2/access_token',
        auth=HTTPBasicAuth(client_id, secret),
        data={'grant_type': 'client_credentials'}
        )

    if debug:
        print_error("Access token result: " + str(response) + str(response.content))

    if response.status_code != 200:
        try:
            message = ERROR_MAP[response.status_code]
        except KeyError:
            message = json_pp(response.json())

        raise BitbucketException(message)

    return response.json()['access_token']

def post_result(url, user, password, verify, data, debug):
    response = requests.post(
        url,
        auth=HTTPBasicAuth(user, password),
        verify=verify,
        json=data
        )

    if debug:
        print_error("Request result: " + str(response.json()))

    # 204 is a success per Bitbucket docs
    if response.status_code != 204:
        try:
            message = ERROR_MAP[response.status_code]
        except KeyError:
            message = json_pp(response.json()) # All other errors, just dump the JSON

        raise BitbucketException(message)

    return response