from requests.auth import HTTPBasicAuth
from requests.packages.urllib3 import disable_warnings as disable_ssl_warnings
from bitbucket import BitbucketDriver
from concourse import ConcourseResource


class BitbucketServerDriver(BitbucketDriver, ConcourseResource):
    def __init__(self, config):
        ConcourseResource.__init__(self, config)
        with self.mandatory_sources('bitbucket_username', 'bitbucket_password', 'bitbucket_url'):
            self.username = config['source']['bitbucket_username']
            self.password = config['source']['bitbucket_password']
            self.endpoint = config['source']['bitbucket_url']
            self.verify_ssl = config['source'].get('verify_ssl', False)

    def get_post_url(self, commit_hash):
        url = '{endpoint}/rest/build-status/1.0/commits/{commit}'.format(
            endpoint=self.endpoint.rstrip('/'),
            commit=commit_hash
        )

        if self.verify_ssl is False:
            disable_ssl_warnings()
            #todo: debug

        return url

    def get_request_options(self):
        return {
            'auth': HTTPBasicAuth(self.username, self.password),
            'verify': self.verify_ssl
        }

    def get_valid_response_status(self):
        return [204]
