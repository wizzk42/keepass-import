"""
UnitTest: close_database
"""

import unittest
from unittest import mock

import importer

from pykeepass import pykeepass as kp


@mock.patch('pykeepass.pykeepass.PyKeePass', autospec=True)
class TestCloseDatabase(unittest.TestCase):
    """
    TestCase: close_database
    """

    def test_close_database_save_success(
        self,
        mock_pykeepass: mock.MagicMock
    ):
        importer.close_database(
            mock_pykeepass,
            True
        )

        mock_pykeepass.save.assert_called_once()

    def test_close_database_save_failure(
        self,
        mock_pykeepass: mock.MagicMock
    ):
        mock_pykeepass.save.side_effect = Exception

        self.assertRaises(
            Exception,
            importer.close_database,
            mock_pykeepass,
            True
        )

        mock_pykeepass.save.assert_called_once()

    def test_close_database_no_save(
        self,
        mock_pykeepass: mock.MagicMock
    ):
        mock_pykeepass.save.side_effect = Exception

        importer.close_database(
            mock_pykeepass,
            False
        )

        mock_pykeepass.save.assert_not_called()
