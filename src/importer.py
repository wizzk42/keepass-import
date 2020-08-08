"""
importer module

Imports a KDBX into another KDBX
"""

import argparse
import calendar
import logging
import shutil
import sys
import time
from typing import List

from pykeepass import pykeepass as kp

DESCRIPTION = ''' Imports Keepass Data into a KDBX database '''


def parse_command_line(args: list):
    """
    Parses the command line arguments
    :param args: The arguments
    :return:
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=DESCRIPTION,
    )
    parser.add_argument(
        'source',
        metavar='SOURCE',
        help='The source database file',
        type=str
    )
    parser.add_argument(
        'target',
        metavar='TARGET',
        help='The target database file',
        type=str
    )
    parser.add_argument(
        '-k', '--source-keyfile',
        dest='source_keyfile',
        help='The keyfile required to decrypt the source database',
        type=str,
        required=False
    )
    parser.add_argument(
        '-l', '--target-keyfile',
        dest='target_keyfile',
        help='The keyfile required to decrypt the target database',
        type=str,
        required=False
    )
    parser.add_argument(
        '-g', '--target-group',
        dest='target_group',
        help='Place all imports in this group in the target database '
             '(defaults to the root group /)',
        type=str,
        default='/',
        required=False
    )
    parser.add_argument(
        '-b', '--backup',
        dest='make_backup',
        help='Backup the target database prior modification',
        action='store_true',
        required=False
    )
    return parser.parse_args(args)


def backup(src: str):
    """
    Creates a backup from src filename to a generated destination
    filename appended with a timestamp
    :param src: source filename
    """
    current_timestamp = str(calendar.timegm(time.gmtime()))
    dst = f"{src}.bak.{current_timestamp}"
    shutil.copyfile(src, dst)


def open_database(filename: str,
                  password: str,
                  keyfile: str or None = None) -> kp.PyKeePass:
    """
    Opens a KDBX database

    :param filename: The database filename
    :param password: The database password
    :param keyfile:  An optional keyfile
    :return: A PyKeePass object
    """
    try:
        return kp.PyKeePass(
            filename,
            password,
            keyfile
        )
    except kp.CredentialsError:
        print('Cannot open database - invalid credentials given.')
        sys.exit(-1)
    except (kp.HeaderChecksumError, kp.PayloadChecksumError):
        print('Checksum mismatch - database corrupt or missing keyfile')
        sys.exit(-1)


def close_database(database: kp.PyKeePass,
                   save=True):
    """
    Closes a KDBX database

    :param database: The database to be closed
    :param save:     Force a save operation prior closing
    """
    if save:
        database.save()
    del database


def _clone_entry(_target_database, _src_entry) -> kp.Entry:
    """ Clones a single entry """
    logging.debug(_src_entry)
    return kp.Entry(
        title=_src_entry.title if _src_entry.title else '',
        username=_src_entry.username if _src_entry.username else '',
        password=_src_entry.password if _src_entry.password else '',
        url=_src_entry.url if _src_entry.url else '',
        notes=_src_entry.notes if _src_entry.notes else '',
        expiry_time=_src_entry.expiry_time if _src_entry.expiry_time else '',
        tags=_src_entry.tags if _src_entry.tags else '',
        icon=_src_entry.icon if _src_entry.icon else '',
        kp=_target_database
    )


def _copy_entries_in_group(_target_database,
                           _src_group) -> List[kp.Entry]:
    """
    Copies all entries in a specific group

    :param _target_database: The target database representation
    :param _src_group:       The source group
    :return:                 A list of copied entries per group
    """
    return [
        _clone_entry(
            _target_database,
            src_entry
        ) for src_entry in _src_group.entries
    ]


def _copy_groups_recursive(_target_database: kp.PyKeePass,
                           _src_group: kp.Group,
                           _dst_parent: kp.Group) -> None:
    """
    Copies a group and all of its subgroups recursively
    along with the entries per subgroup

    :param _target_database:    The target database
    :param _src_group:         The source parent group
    :param _dst_parent:         The target parent group
    :return:
    """
    dst_group = _target_database.add_group(
        _dst_parent,
        _src_group.name,
        _src_group.icon,
        _src_group.notes
    )
    if _src_group.subgroups:
        for src_subgroup in _src_group.subgroups:
            _copy_groups_recursive(
                _target_database,
                src_subgroup,
                dst_group
            )
    if _src_group.entries:
        entries = _copy_entries_in_group(
            _target_database,
            _src_group
        )
        dst_group.append(entries)


def import_entries(target_database: kp.PyKeePass,
                   source_database: kp.PyKeePass) -> None:
    """
    Imports entries from the source database into a target database

    :param target_database: The target database where entries
                            get imported
    :param source_database: The source database which provides
                            entries to be imported
    """
    current_import_ts = calendar.timegm(time.gmtime())
    import_group = target_database.add_group(
        target_database.root_group,
        f'__imported__{current_import_ts}'
    )

    _copy_groups_recursive(
        target_database,
        source_database.root_group,
        import_group
    )


def read_password(prompt='Password: ') -> str:
    """
    Reads a password from a CLI prompt

    :param prompt: The prompt string presented to the user
    :return:       The data entered by the user
    """
    return input(prompt)


def configure_logging():
    """ Initialize logging """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


def run(args: list) -> int:
    """
    Runs the import

    :param args: The cli arguments
    :return:     An exit code: Anything but 0 will indicate some error
    """
    configure_logging()
    cli = parse_command_line(args)

    if cli.make_backup:
        backup(cli.target)

    source_password = read_password('Password for Source database: ')
    target_password = read_password('Password for Target database: ')

    source_database = open_database(
        cli.source,
        source_password,
        cli.source_keyfile
    )
    target_database = open_database(
        cli.target,
        target_password,
        cli.target_keyfile
    )

    import_entries(target_database, source_database)

    close_database(target_database, True)
    close_database(source_database, False)

    return 0
