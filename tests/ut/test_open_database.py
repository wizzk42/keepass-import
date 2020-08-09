import unittest
from unittest import mock

import importer

from pykeepass import pykeepass as kp


@mock.patch('pykeepass.pykeepass.PyKeePass', autospec=True)
class TestOpenDatabase(unittest.TestCase):
    """
    TestCase: open_database
    """

    def test_open_database_success(
        self,
        mock_pykeepass: mock.MagicMock
    ):
        mock_pykeepass.return_value = 'test-object'

        mock_filename, mock_password, mock_keyfile = self._init_mocks()

        result = importer.open_database(
            mock_filename,
            mock_password,
            mock_keyfile
        )

        mock_pykeepass.assert_called_once()
        self.assertEqual(result, 'test-object')

    def test_open_database_invalid_credentials(
        self,
        mock_pykeepass: mock.MagicMock
    ):
        mock_pykeepass.side_effect = kp.CredentialsError()

        mock_filename, mock_password, mock_keyfile = self._init_mocks()

        self.assertRaises(
            SystemExit,
            importer.open_database,
            mock_filename,
            mock_password,
            mock_keyfile
        )

        mock_pykeepass.assert_called_once()

    def test_open_database_invalid_header_checksum(
        self,
        mock_pykeepass: mock.MagicMock
    ):
        mock_pykeepass.side_effect = kp.HeaderChecksumError()

        mock_filename, mock_password, mock_keyfile = self._init_mocks()

        self.assertRaises(
            SystemExit,
            importer.open_database,
            mock_filename,
            mock_password,
            mock_keyfile
        )

        mock_pykeepass.assert_called_once()

    def test_open_database_invalid_payload_checksum(
        self, mock_pykeepass: mock.MagicMock
    ):
        mock_pykeepass.side_effect = kp.PayloadChecksumError()

        mock_filename, mock_password, mock_keyfile = self._init_mocks()

        self.assertRaises(
            SystemExit,
            importer.open_database,
            mock_filename,
            mock_password,
            mock_keyfile)

        mock_pykeepass.assert_called_once()

    @staticmethod
    def _init_mocks():
        mock_filename = mock.MagicMock()
        mock_filename.return_value = 'sample-file'
        mock_password = mock.MagicMock()
        mock_password.return_value = 'sample-pass'
        mock_keyfile = mock.MagicMock()
        mock_keyfile.return_value = 'sample-keyfile'
        return mock_filename, mock_password, mock_keyfile
