"""
UnitTest: read_password
"""

import unittest
from unittest import mock

import importer


@mock.patch('importer.getpass', autospec=True)
class TestReadPassword(unittest.TestCase):
    """
    TestCase: read_password
    """

    def test_read_password(
        self,
        mock_getpass: mock.MagicMock
    ):
        mock_getpass.return_value = 'sample-password'

        result = importer.read_password('sample prompt: ')

        mock_getpass.assert_called_once()

        self.assertEqual(result, 'sample-password')
