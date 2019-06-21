import unittest
import mock
import requests

from bitbucket import request_access_token, BitbucketException


class RequestAccessTokenTestCase(unittest.TestCase):

    def test_fails_ok(self):
        with mock.patch('requests.post') as post:
            r = mock.MagicMock()
            r.status_code = 401
            r.json.return_value = {}

            post.return_value = r

            with self.assertRaises(BitbucketException):
                request_access_token('client', 'secret', False)

    def test_works(self):
        with mock.patch('requests.post') as post:
            r = mock.MagicMock()
            r.status_code = 200
            r.json.return_value = {"access_token": "token"}

            post.return_value = r

            self.assertEqual(
                request_access_token('client', 'secret', False),
                "token"
            )
