from requests.auth import HTTPBasicAuth
from requests.packages.urllib3 import disable_warnings as disable_ssl_warnings
from bitbucket import BitbucketDriver
from concourse import ConcourseResource, MissingSourceException, print_error


class BitbucketServerDriver(BitbucketDriver, ConcourseResource):
    def __init__(self, config, debug):
        ConcourseResource.__init__(self, config)
        self.debug = debug
        self.username = config['source'].get('username', config['source'].get('bitbucket_username', ''))
        self.password = config['source'].get('password', config['source'].get('bitbucket_password', ''))
        self.endpoint = config['source'].get('endpoint', config['source'].get('bitbucket_url', ''))
        self.verify_ssl = config['source'].get('verify_ssl', False)

        if self.username == '':
            raise MissingSourceException('username')

        if self.password == '':
            raise MissingSourceException('password')

        if self.endpoint == '':
            raise MissingSourceException('endpoint')

    def get_post_url(self, commit_hash):
        url = '{endpoint}/rest/build-status/1.0/commits/{commit}'.format(
            endpoint=self.endpoint.rstrip('/'),
            commit=str(commit_hash)
        )

        if self.verify_ssl is False:
            disable_ssl_warnings()
            if self.debug:
                print_error("SSL warnings disabled\n")

        return url

    def get_request_options(self):
        return {
            'auth': HTTPBasicAuth(self.username, self.password),
            'verify': self.verify_ssl
        }

    def get_valid_response_status(self):
        return [204]
