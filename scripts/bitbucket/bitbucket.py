#!/usr/bin/env python

import sys
import json
import requests
from abc import ABCMeta, abstractmethod
from requests.auth import HTTPBasicAuth, AuthBase

ERROR_MAP = {
    403: "HTTP 403 Forbidden - Does your bitbucket user have rights to the repo?",
    404: "HTTP 404 Not Found - Does the repo supplied exist?",
    400: "HTTP 401 Unauthorized - Are your bitbucket credentials correct?"
}


class BitbucketException(Exception): pass


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

    def __call__(self, r):
        r.headers['Authorization'] = "Bearer {}".format(self.access_token)
        return r


# Convenience method for writing to stderr. Coerces input to a string.
def err(txt):
    sys.stderr.write(str(txt) + "\n")


# Convenience method for pretty-printing JSON
def json_pp(json_object):
    if isinstance(json_object, dict):
        return json.dumps(json_object,
                   sort_keys=True,
                   indent=4,
                   separators=(',', ':')) + "\n"
    elif isinstance(json_object, str):
        return json.dumps(json.loads(json_object),
                   sort_keys=True,
                   indent=4,
                   separators=(',', ':')) + "\n"
    else:
        raise NameError('Must be a dictionary or json-formatted string')


def set_build_status(repo, commit_hash, state, key, name, url, description,
                     debug, driver, endpoint, username, password, verify_ssl):

    post_url = driver.get_post_url(commit_hash)

    data = {
        "state": state,
        "key": key,
        "name": name,
        "url": url,
        "description": description
    }

    r = requests.post(
        post_url,
        json=data,
        **driver.get_request_options()
    )

    if debug:
        err("Request result: " + str(r))

    # Check status code. Bitbucket brakes rest a bit  by returning 200 or 201
    # depending on it's the first time the status is posted.
    if r.status_code not in driver.get_valid_response_status():
        try:
            msg = ERROR_MAP[r.status_code]
        except KeyError:
            msg = json_pp(r.json())

        raise BitbucketException(msg)


def request_access_token(client_id, secret, debug):
    r = requests.post(
        'https://bitbucket.org/site/oauth2/access_token',
        auth=HTTPBasicAuth(client_id, secret),
        data={'grant_type': 'client_credentials'}
        )

    if debug:
        err("Access token result: " + str(r) + str(r.content))

    if r.status_code != 200:
        try:
            msg = ERROR_MAP[r.status_code]
        except KeyError:
            msg = json_pp(r.json())

        raise BitbucketException(msg)

    return r.json()['access_token']
