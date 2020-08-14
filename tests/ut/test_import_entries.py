"""
UnitTest: import_entries
"""

import unittest
from unittest import mock

import importer


class TestImportEntries(unittest.TestCase):
    """
    TestCase: import_entries
    """

    @mock.patch('importer._copy_groups_recursive')
    def test_import_entries_empty_database(
        self,
        mock_copy_groups: mock.MagicMock
    ):
        mock_pykeepass_source = mock.MagicMock()
        mock_pykeepass_source.root_group = mock.MagicMock()

        mock_pykeepass_target = mock.MagicMock()
        mock_pykeepass_target.root_group = mock.MagicMock()

        importer.import_entries(
            mock_pykeepass_target,
            mock_pykeepass_source
        )

        mock_pykeepass_target.add_group.assert_called()
        mock_copy_groups.assert_called()
        self.assertEqual(len(mock_pykeepass_target.groups), 0)
