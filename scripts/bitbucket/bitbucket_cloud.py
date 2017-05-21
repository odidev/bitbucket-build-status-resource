from bitbucket import BitbucketDriver, BitbucketOAuth, request_access_token
from concourse import ConcourseResource, MissingSourceException


class BitbucketCloudDriver(BitbucketDriver, ConcourseResource):
    def __init__(self, config):
        ConcourseResource.__init__(self, config)
        with self.mandatory_sources('client_id', 'secret'):
            self.repository = config['source'].get(
                'repo',
                '{owner}/{repository}'.format(
                    owner=config['source'].get(
                        'owner',
                        config['source'].get('bitbucket_username', '')
                    ),
                    repository=config['source'].get(
                        'repository_name',
                        config['params']['repo']
                    )
                )
            )
            self.client_id = config['source']['client_id']
            self.cliend_secret = config['source']['secret']

            if self.repository == '':
                raise MissingSourceException('repo')

    def get_post_url(self, commit_hash):
        return 'https://api.bitbucket.org/2.0/repositories/{repository}/commit/{commit}/statuses/build'.format(
            repository=self.repository,
            commit=commit_hash
        )

    def get_request_options(self):
        access_token = request_access_token(self.client_id, self.client_secret, False)

        return {
            'auth': BitbucketOAuth(access_token)
        }

    def get_valid_response_status(self):
        return [200, 201]
