"""
UnitTest: backup
"""

import unittest
from unittest import mock

import importer


@mock.patch('shutil.copyfile', autospec=True)
class TestBackup(unittest.TestCase):
    """
    TestCase: open_database
    """

    def test_backup_success(
        self,
        mock_shutil_copyfile: mock.MagicMock
    ):
        mock_shutil_copyfile.return_value = None
        mock_filename = mock.MagicMock()
        mock_filename.return_value = 'mock-filename'

        importer.backup(mock_filename)

        mock_shutil_copyfile.assert_has_calls(
            mock_shutil_copyfile.call_args_list
        )

    def test_backup_failure(
        self,
        mock_shutil_copyfile: mock.MagicMock
    ):
        mock_shutil_copyfile.side_effect = Exception
        mock_filename = mock.MagicMock()
        mock_filename.return_value = 'mock-filename'

        self.assertRaises(Exception, importer.backup, mock_filename)

        mock_shutil_copyfile.assert_has_calls(
            mock_shutil_copyfile.call_args_list
        )
